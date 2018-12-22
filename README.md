# サンプリングデータ作成

params.jsonのパラメタリストを編集する。
k_aveは偶数になるように！

python make-params.py
全パラメタ組み合わせファイル(resource/params-all.csv)と
最大サンプリング行のみファイル(resource/params-max-sampling.csv)を作成する。

Rscript make-data-1.R | tee resource/log/make-data-1.log
最大サンプリングの条件のみ計算する。

Rscript make-data-2.R | tee resource/log/make-data-2.log
最大サンプリングよりサブサンプリングする。


# 相関分析

## mic

sh mkdir.sh
保存用ディレクトリを作成する。
ファイル内で、iter_numを指定する。

Rscript main.R | tee out-res/main.log
計算する。

python mapping-save-data.py | tee out-res/mapping.log
iter毎のaucをまとめる。

## spiec-easi

sh mkdir.sh
保存用ディレクトリを作成する。
ファイル内で、iter_numを指定する。

Rscript main.R | tee out-res/main.log
計算する。

python mapping-save-data.py | tee out-res/mapping.log
iter毎のaucをまとめる。

## rebacca

sh mkdir.sh
保存用ディレクトリを作成する。
ファイル内で、iter_numを指定する。

Rscript main.R | tee out-res/main.log
計算する。

python mapping-save-data.py | tee out-res/mapping.log
iter毎のaucをまとめる。

## cclasso

sh mkdir.sh
保存用ディレクトリを作成する。
ファイル内で、iter_numを指定する。

Rscript main.R | tee out-res/main.log
計算する。

python mapping-save-data.py | tee out-res/mapping.log
iter毎のaucをまとめる。

## general

sh mkdir.sh
保存用ディレクトリを作成する。
ファイル内で、iter_numを指定する。

Rscript main.R | tee out-res/main.log
計算する。

python mapping-save-data.py | tee out-res/mapping.log
iter毎のaucをまとめる。

## sparcc

sh clean-mkdir.sh
保存用ディレクトリを作成する。
ファイル内で、iter_numを指定する。

Rscript main.R | tee out-res/main.log
計算する。

python mapping-save-data.py | tee out-res/mapping.log
iter毎のaucをまとめる。