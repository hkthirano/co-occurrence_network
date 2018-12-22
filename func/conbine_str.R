# pasteによる連結を簡単にする
L <- function(..., sep = "", collapse = NULL) {
    paste(..., sep = sep, collapse = collapse)
}

L2 <- function(..., sep = "/", collapse = NULL) {
    paste(..., sep = sep, collapse = collapse)
}