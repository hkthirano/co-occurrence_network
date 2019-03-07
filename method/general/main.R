source("../../func/conbine_str.R")
source("../../func/dataloader.R")
library(doParallel)
library(foreach)
library(pROC)
library(PRROC)
library(jsonlite)
library(ppcor)



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
calc_cat_auc <- function(network_pred, real, id, iter, method){
    # 対角要素を０に
    diag(network_pred) <- 0

    # only use elements in lower triangular matrix
    pred <- network_pred[lower.tri(network_pred)]

    # rocの計算
    roc <- roc(real, pred)$auc
    prc <- pr.curve(pred[real == 1],pred[real == 0])$auc.integral

    #iter毎のaucを保存
    file_name <- L("out-res/iter-", iter, "/id-", id, "-", method, ".txt")
    cat(roc, prc, "\n", file=file_name)
}



calc_general <- function( params_i, iter ){
    id <- params_i[, "id"]
    err <- 0

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

        # === count ===

        # @@@@@@@@@@ 1 count-pea @@@@@@@@@@
        #tryCatch({
        #    network_pred <- abs(cor(t(count_data)))
        #    calc_cat_auc(network_pred, real, id, iter, "count-pea")
        #},
        #error = function(e) {
        #    cat("\n\nid -", id, " | 1 count-pea は計算できなかった！\n\n")
        #    err <- 1
        #})

        # @@@@@@@@@@ 2 count-spe @@@@@@@@@@
        #tryCatch({
        #    network_pred <- abs(cor(t(count_data),m="s"))
        #    calc_cat_auc(network_pred, real, id, iter, "count-spe")
        #},
        #error = function(e) {
        #    cat("\n\nid -", id, " | 2 count-spe は計算できなかった！\n\n")
        #    err <- 1
        #})

        # @@@@@@@@@@ 3 count-ppea @@@@@@@@@@
        #tryCatch({
        #    network_pred <- abs(pcor(t(count_data))$estimate)
        #    calc_cat_auc(network_pred, real, id, iter, "count-ppea")
        #},
        #error = function(e) {
        #    cat("\n\nid -", id, " | 3 count-ppea は計算できなかった！\n\n")
        #    err <- 1
        #})

        # @@@@@@@@@@ 4 count-pspe @@@@@@@@@@
        #tryCatch({
        #    network_pred <- abs(pcor(t(count_data),m="s")$estimate)
        #    calc_cat_auc(network_pred, real, id, iter, "count-pspe")
        #},
        #error = function(e) {
        #    cat("\n\nid -", id, " | 4 count-pspe は計算できなかった！\n\n")
        #    err <- 1
        #})

        # @@@@@@@@@@ 5 flac-pea @@@@@@@@@@
        tryCatch({
            network_pred <- abs(cor(t(flac_data)))
            calc_cat_auc(network_pred, real, id, iter, "flac-pea")
        },
        error = function(e) {
            cat("\n\nid -", id, " | 5 flac-pea は計算できなかった！\n\n")
            err <- 1
        })

        # @@@@@@@@@@ 6 flac-spe @@@@@@@@@@
        tryCatch({
            network_pred <- abs(cor(t(flac_data),m="s"))
            calc_cat_auc(network_pred, real, id, iter, "flac-spe")
        },
        error = function(e) {
            cat("\n\nid -", id, " | 6 flac-spe は計算できなかった！\n\n")
            err <- 1
        })

        # @@@@@@@@@@ 7 flac-ppea @@@@@@@@@@
        tryCatch({
            network_pred <- abs(pcor(t(flac_data))$estimate)
            calc_cat_auc(network_pred, real, id, iter, "flac-ppea")
        },
        error = function(e) {
            cat("\n\nid -", id, " | 7 flac-ppea は計算できなかった！\n\n")
        })

        # @@@@@@@@@@ 8 flac-pspe @@@@@@@@@@
        tryCatch({
            network_pred <- abs(pcor(t(flac_data),m="s")$estimate)
            calc_cat_auc(network_pred, real, id, iter, "flac-pspe")
        },
        error = function(e) {
            cat("\n\nid -", id, " | 8 flac-pspe は計算できなかった！\n\n")
            err <- 1
        })

        # ８手法のどれかでエラーが起きたとき
        if (err == 1){
            cat("\n\n")
            print(params_i)
            cat("\n\n")
        }
    },

    error = function(e) {
        cat("\n\nid -", id, "はcountデータがなかった！\n\n")
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
        calc_general( params[i, ], iter )
    }
}

stopCluster(cluster)

cat("\n\n======== 完了 ========\n\n")