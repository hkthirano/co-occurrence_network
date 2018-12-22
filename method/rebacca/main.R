source("../../func/conbine_str.R")
source("../../func/dataloader.R")
source("R/REBACCA_main.R")
source("R/REBACCA_simulation_model.R")
require(MCMCpack)
require(glmnet)
library(pROC)
library(PRROC)
library(jsonlite)
library(doParallel)



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



# === 関数 ===
calc_rebacca <- function( params_i, iter ){
    id <- params_i[, "id"]

    tryCatch({
        # network_realとcountデータの読み込み
        obj <- dataloader_real_A_count_v2( params_i, iter )

        # 正解ラベル
        network_real <- obj[[1]]
        real <- network_real[lower.tri(network_real)]

        # countデータ
        count_data <- obj[[3]]
        # flacデータ
        flac_data <- t(t(count_data) / apply(count_data,2,sum))

        # rebbacaの計算
        x.rslt <- rebacca(flac_data, nbootstrap=50)
        network_pred <- x.rslt$Stability
        #tau <- stability_cutoff(x.rslt$Stability, x.rslt$q, B=50, FWER=0.05)
        #x.adj <- sscore2adjmatrix(x.rslt$Stability, tau)
        #network_pred <- rebacca_adjm2corr(flac_data, x.adj)$corr
        
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
         
        cat("\n\nid -", id, "は計算できた！\n\n")
    },
    # 計算できなかった時
    error = function(e) {
        cat("\n\n")
        print(params_i)
        cat("\n\n")
        cat("\n\nid -", id, "は計算できなかった！\n\n")
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
        calc_rebacca( params[i, ], iter )

    }
}

stopCluster(cluster)

cat("\n\n======== 完了 ========\n\n")