source("func/generateA_specific_type.R")
source("func/conbine_str.R")
source("func/save_sampling.R")
source("func/dataloader.R")
library(jsonlite)
library(seqtime)
library(doParallel)
library(foreach)



# === 必要データ準備 ===
params_json <- read_json("/Users/hirano/Sites/new-main/resource/params.json")

iter_num <- params_json$`iter-num`

params_file_path <- params_json$`params-all-csv`
params <- read.csv(params_file_path)
n_row <- nrow(params)

sampling_len <- length(params_json$`sampling`)
end_i <- n_row / sampling_len

cores = detectCores()
cluster = makeCluster(cores, 'FORK', outfile="")
registerDoParallel(cluster)



# === 関数 ===
random_sampling <- function( max_sampling_i, sampling_len, iter ){
    # メイン
    tryCatch({
        # network_realとcountデータの読み込み
        obj <- dataloader_real_A_count( params[max_sampling_i,], iter ) # 最大サンプリング

        count_data <- obj[[3]]

        next_i <- max_sampling_i
        for ( j in 1:(sampling_len-1) ){

            next_i <- next_i + 1
            ix <- sample( 1:ncol(count_data), params[next_i, "sampling"] )
            count_data <- count_data[, ix]

            # データ保存
            save_sampling(count_data, obj, params[next_i, ], iter)
        }
    },

    error = function(e) {
        #cat("\n\n")
        #print(params[max_sampling_i,])
        #cat("\n\n")
        id <- params[max_sampling_i, "id"]
        cat("\n\nid -", id, "はサンプリングデータがなかった！\n\n")
    })
}



# === メイン ===

# iter回数繰り返す
for ( iter in 1:iter_num ){

    # 条件毎に繰り返す => 各条件に１コアを与える（計２４コアー２４条件ずつ）
    #foreach ( i = seq_len(end_i) ) %do% { # 並列なし
    foreach ( i = seq_len(end_i) ) %dopar% { # 並列あり

        if ( (i %% 50) == 0 ){
            cat("\n\n==================== iter - ", iter, " ====================\n\n")
        }

        # 最大サンプリングのみを指定していく
        max_sampling_i <- 1+sampling_len*(i-1) # 等差数列
        random_sampling( max_sampling_i, sampling_len, iter )

    }
}

stopCluster(cluster)

cat("======== 完了 ========\n")