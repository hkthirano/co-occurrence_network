source("../../func/conbine_str.R")
source("../../func/dataloader.R")
library(doParallel)
library(foreach)
library(minerva)
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



# === 関数 ===
calc_mic <- function( params_i, iter ){
    id <- params_i[, "id"]

    # === count ===
    #tryCatch({
        # network_realとcountデータの読み込み
        obj <- dataloader_real_A_count_v2( params_i, iter )

        # 正解ラベル
        network_real <- obj[[1]]
        real <- network_real[lower.tri(network_real)]

        # countデータ
        count_data <- obj[[3]]

        # micの計算
        #network_pred_count <- mine( t(count_data) )$MIC

        # 絶対値に
        #network_pred_count <- abs(network_pred_count)
        # 対角要素を０に
        #diag(network_pred_count) <- 0

        # only use elements in lower triangular matrix
        #pred_count <- network_pred_count[lower.tri(network_pred_count)]

        # roc,prcの計算
        #roc_count <- roc(real, pred_count)$auc
        #prc_count <- pr.curve(pred_count[real == 1],pred_count[real == 0])$auc.integral

        #iter毎のaucを保存
        #file_name_count <- L("out-res/iter-", iter, "/id-", id, "-count-mic.txt")
        #cat(roc_count, prc_count, "\n", file=file_name_count)
         
        #cat("\n\n[count] id -", id, "は計算できた！\n\n")
    #},
    # 計算できなかった時
    #error = function(e) {
    #    cat("\n\n")
    #    print(params_i)
    #    cat("\n\n")
    #    cat("\n\n[count] id -", id, "は計算できなかった！\n\n")
    #}) 


    # === flac ===
    tryCatch({
        # flacデータ
        flac_data <- t(t(count_data) / apply(count_data,2,sum))
        
        # micの計算
        network_pred_flac <- abs( mine( t(flac_data) )$MIC )

        # 絶対値に
        network_pred_flac <- abs(network_pred_flac)
        # 対角要素を０に
        diag(network_pred_flac) <- 0

        # only use elements in lower triangular matrix
        pred_flac <- network_pred_flac[lower.tri(network_pred_flac)]

        # roc,prcの計算
        roc_flac <- roc(real, pred_flac)$auc
        prc_flac <- pr.curve(pred_flac[real == 1],pred_flac[real == 0])$auc.integral

        #iter毎のaucを保存
        file_name_flac <- L("out-res/iter-", iter, "/id-", id, "-flac-mic.txt")
        cat(roc_flac, prc_flac, "\n", file=file_name_flac)
         
        cat("\n\n[flac] id -", id, "は計算できた！\n\n")
    },
    # 計算できなかった時
    error = function(e) {
        cat("\n\n")
        print(params_i)
        cat("\n\n")
        cat("\n\n[flac] id -", id, "は計算できなかった！\n\n")
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
        calc_mic( params[i, ], iter )
    }
}

stopCluster(cluster)

cat("\n\n======== 完了 ========\n\n")