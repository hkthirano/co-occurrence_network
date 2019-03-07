source("/Users/hirano/Sites/new-main/func/conbine_str.R")


# /make_data.Rで使用
save_sampling <- function(count_data, obj, params_i, iter){
    network <- as.character(params_i[, "network"])
    interact <- as.character(params_i[, "interact"])
    nn <- params_i[, "nn"]
    k_ave <- params_i[, "k.ave"]
    s_max <- params_i[, "s.max"]
    sampling <- params_i[, "sampling"]
    mode <- as.character(params_i[, "mode"])
    file_name <- params_i[, "file.name"]

    # network real
    network_real <- obj[[1]]
    # interaction matrix for gLV model
    A <- obj[[2]]

    # network real保存
    real_dir <- L("data/",network,"/",interact,"/mode-",mode,"/iter-",iter,"/real/",file_name)
    #cat("保存先",real_dir,"\n")
    write.table(network_real, real_dir, quote=F, sep="\t", row.names=F, col.names=F)

    # A保存
    A_dir <- L("data/",network,"/",interact,"/mode-",mode,"/iter-",iter,"/A/",file_name)
    cat("保存先",A_dir,"\n")
    write.table(A, A_dir, quote=F, sep="\t", row.names=F, col.names=F)

    # countデータ保存
    count_dir <- L("data/",network,"/",interact,"/mode-",mode,"/iter-",iter,"/count/",file_name)
    cat("保存先",count_dir,"\n")
    write.table(count_data, count_dir, quote=F, sep="\t",row.names=T)
}    
