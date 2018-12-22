source("/Users/hirano/Sites/new-main/func/conbine_str.R")



# make-data-1.Rで使用
dataloader_real_A_count <- function( params_i, iter ){
    network <- as.character(params_i[, "network"])
    interact <- as.character(params_i[, "interact"])
    file_name <- as.character(params_i[, "file.name"])
    # network_realの読み込み
    network_real_file <- L("data/", network,"/",interact,"/iter-",iter,"/real/",file_name)
    network_real = read.table(network_real_file)
    #print(L("読んだファイル : ", network_real_file))
    
    # Aの読み込み
    A_file <- L("data/", network,"/",interact,"/iter-",iter,"/A/",file_name)
    A = read.table(A_file)
    #print(L("読んだファイル : ", A_file))

    # countデータの読み込み
    count_data_file <- L("data/", network,"/",interact,"/iter-",iter,"/count/",file_name)
    count_data = read.table(count_data_file, header=T, row.names=1)
    #print(L("読んだファイル : ", count_data_file))

    return(list(network_real, A, count_data))
}



# 相関分析で使用
# pathを変更 data => ../../data
dataloader_real_A_count_v2 <- function( params_i, iter ){
    network <- as.character(params_i[, "network"])
    interact <- as.character(params_i[, "interact"])
    file_name <- as.character(params_i[, "file.name"])

    # network_realの読み込み
    network_real_file <- L("../../data/", network,"/",interact,"/iter-",iter,"/real/",file_name)
    network_real = read.table(network_real_file)
    #print(L("読んだファイル : ", network_real_file))
    
    # Aの読み込み
    A_file <- L("../../data/", network,"/",interact,"/iter-",iter,"/A/",file_name)
    A = read.table(A_file)
    #print(L("読んだファイル : ", A_file))

    # countデータの読み込み
    count_data_file <- L("../../data/", network,"/",interact,"/iter-",iter,"/count/",file_name)
    count_data = read.table(count_data_file, header=T, row.names=1)
    #print(L("読んだファイル : ", count_data_file))

    return(list(network_real, A, count_data))
}


# sparccで使用
dataloader_real_pred <- function( params_i, iter ){
    network <- as.character(params_i[, "network"])
    interact <- as.character(params_i[, "interact"])
    file_name <- as.character(params_i[, "file.name"])

    # network_realの読み込み
    network_real_file <- L("../../data/", network,"/",interact,"/iter-",iter,"/real/",file_name)
    network_real = read.table(network_real_file)
    #print(L("読んだファイル : ", network_real_file))

    # network_predの読み込み
    network_pred_file <- L("../../data/", network,"/",interact,"/iter-",iter,"/pred/sparcc/",file_name)
    network_pred = read.table(network_pred_file)
    #print(L("読んだファイル : ", network_pred_file))

    return(list(network_real, network_pred))
}