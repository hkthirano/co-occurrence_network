source("func/generateA_specific_type.R")
source("func/conbine_str.R")
source("func/save_sampling.R")
library(doParallel)
library(foreach)
library(jsonlite)
library(seqtime)



# === 必要データ準備 ===
params_json <- read_json("/Users/hirano/Sites/new-main/resource/params.json")

iter_num <- params_json$`iter-num`

max_sampling_params_file_path <- params_json$`params-max-sampling-csv`
params <- read.csv(max_sampling_params_file_path)
n_row <- nrow(params)

cores = detectCores()
cluster = makeCluster(cores, 'FORK', outfile="")
registerDoParallel(cluster)



# === 関数 ===
make_data <- function( params_i, iter ){
    id <- params_i[, "id"]
    network <- as.character(params_i[, "network"])
    interact <- as.character(params_i[, "interact"])
    nn <- params_i[, "nn"]
    k_ave <- params_i[, "k.ave"]
    s_max <- params_i[, "s.max"]
    sampling <- params_i[, "sampling"]
    ratio <- params_i[, "ratio"] / 10

    # メイン
    tryCatch({
        ## Genrate matrices
        obj <- generateA_specific_type(nn, k_ave, type.network=network, type.interact=interact, interact.str.max=s_max, mix.compt.ratio=ratio)

        # interaction matrix for gLV model
        A <- obj[[2]]

        # Generate dataset on species abundance using gLV model
        capture.output( count_data <- generateDataSet(sampling, A, count=100*nn) )# 警告が長いので出力しない

        # データ保存
        save_sampling(count_data, obj, params_i, iter)

        cat("\n\nid -", id, "は計算できた！\n\n")
    },

    # 計算できなかった時
    # networkが構築できない、発散する等
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
            cat("\n\n==================== iter - ", iter, " ====================\n\n")
        }

        make_data( params[i, ], iter )

    }
}

stopCluster(cluster)

cat("======== 完了 ========\n")
