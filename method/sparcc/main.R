source("../../func/conbine_str.R")
source("../../func/dataloader.R")
library(doParallel)
library(foreach)
library(devtools)
library(pROC)
library(PRROC)
library(jsonlite)



# === 必要データ準備 ===
params_json <- read_json("/Users/hirano/Sites/new-main/resource/params.json")

iter_num <- params_json$`iter-num`

# 基準params
params_file_path <- params_json$`params-all-csv`
params <- read.csv(params_file_path)
n_row <- nrow(params)

cores = detectCores()
cluster = makeCluster(cores, 'FORK', outfile="")
registerDoParallel(cluster)

python <- "/Users/hirano/.pyenv/versions/2.7-dev/bin/python"
arg_1 <- "lib/SparCC.py"



# === 関数 ===
calc_sparcc <- function( params_i, iter ){
    id <- params_i[, "id"]
    network <- as.character(params_i[, "network"])
    interact <- as.character(params_i[, "interact"])
    sampling <- params_i[, "sampling"]
    file_name <- params_i[, "file.name"]


    tryCatch({
        # sparccを計算して相関行列を保存
        arg_2 <- L("../../data/", network, "/", interact, "/iter-", iter, "/count/", file_name)
        arg_3 <- L("--cor_file=../../data/", network, "/", interact, "/iter-", iter, "/pred/sparcc/", file_name)

        cmd = L(python, " ", arg_1, " ", arg_2, " ", arg_3)
        # 実際にシェルからプログラム実行
        # 計算できなくてもtryCatchには引っかからない
        system(cmd)

        # network_realとnetwork_predデータの読み込み
        obj <- dataloader_real_pred( params_i, iter )

        # 正解ラベル
        network_real <- obj[[1]]
        real <- network_real[lower.tri(network_real)]

        # 相関行列結果
        network_pred <- obj[[2]]

        # 絶対値に
        network_pred <- abs(network_pred)
        # 対角要素を０に
        diag(network_pred) <- 0

        # only use elements in lower triangular matrix
        pred <- network_pred[lower.tri(network_pred)]

        # rocの計算
        roc <- roc(real, pred)$auc
        prc <- pr.curve(pred[real == 1],pred[real == 0])$auc.integral

        #iter毎のaucを保存
        file_name <- L("out-res/iter-", iter, "/id-", id, ".txt")
        cat(roc, prc, "\n", file=file_name)

        cat("\n\n========== id -", id, "は計算できた！ ==========\n\n")
    },
    # 計算できなかった時
    error = function(e) {
        cat("\n\n")
        print(params_i)
        cat("\n\n")
        cat("\n\n\n\n========== id -", id, "は計算できなかった！==========n\n\n\n")
    }) 
}



# === メイン ===

# iter回数繰り返す
for ( iter in 1:iter_num ){

    # 条件毎に繰り返す => 各条件に１コアを与える（計２４コアー２４条件ずつ）
    #foreach ( i = seq_len(n_row) ) %do% { # 並列なし
    foreach ( i = seq_len(n_row) ) %dopar% { # 並列あり

        if ( (i %% 50) == 0 ){
            cat("\n\n==================== iter - ", iter, " | id - ", params[i, "id"], "====================\n\n")
        }

        # 相関分析を行い、iter毎にrocとprcを保存する
        calc_sparcc( params[i, ], iter )
    }
}

stopCluster(cluster)

cat("\n\n======== 完了 ========\n\n")
