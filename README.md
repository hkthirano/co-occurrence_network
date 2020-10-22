# 注意

`HOME/Sites/`以下にこのレポジトリを置かないと動かない。

# サンプリングデータ作成

params.jsonのパラメタリストを編集する。  
k_aveは偶数になるように！

`sh bin/make-dir.sh`  
保存用ディレクトリを作成する(デフォルト30iter)。

`mkdir resource/tmp`  
ディレクトリ作成。

`python make-params.py`  
全パラメタ組み合わせファイル(resource/params-all.csv)と  
最大サンプリング行のみファイル(resource/tmp/params-max-sampling.csv)を作成する。

`Rscript make-data-1.R | tee resource/log/make-data-1.log`  
最大サンプリングの条件のみ計算する。

`Rscript make-data-2.R | tee resource/log/make-data-2.log`  
最大サンプリングよりサブサンプリングする。


# 相関分析

## mic

`sh mkdir.sh`  
保存用ディレクトリを作成する(デフォルト30iter)。  

`Rscript main.R | tee out-res/main.log`  
相関分析。

`python mapping-save-data.py count-mic | tee out-res/mapping-count-mic.log`  
`python mapping-save-data.py flac-mic | tee out-res/mapping-flac-mic.log`  
相関分析結果csvファイルの作成。

## spiec-easi

`sh mkdir.sh`  
保存用ディレクトリを作成する(デフォルト30iter)。  

`Rscript main.R | tee out-res/main.log`  
相関分析。

`python mapping-save-data.py | tee out-res/mapping.log`  
相関分析結果csvファイルの作成。

## rebacca

`sh mkdir.sh`  
保存用ディレクトリを作成する(デフォルト30iter)。

`Rscript main.R | tee out-res/main.log`  
相関分析。

`python mapping-save-data.py | tee out-res/mapping.log`  
相関分析結果csvファイルの作成。

## cclasso

`sh mkdir.sh`  
保存用ディレクトリを作成する(デフォルト30iter)。

`Rscript main.R | tee out-res/main.log`  
相関分析。

`python mapping-save-data.py | tee out-res/mapping.log`  
相関分析結果csvファイルの作成。

## general

`sh mkdir.sh`  
保存用ディレクトリを作成する(デフォルト30iter)。

`Rscript main.R | tee out-res/main.log`  
相関分析。

`python mapping-save-data.py count-pea | tee out-res/mapping-count-pea.log`  
`python mapping-save-data.py count-spe | tee out-res/mapping-count-spe.log`  
`python mapping-save-data.py count-ppea | tee out-res/mapping-count-ppea.log`  
`python mapping-save-data.py count-pspe | tee out-res/mapping-count-pspe.log`  
`python mapping-save-data.py flac-pea | tee out-res/mapping-flac-pea.log`  
`python mapping-save-data.py flac-spe | tee out-res/mapping-flac-spe.log`  
`python mapping-save-data.py flac-ppea | tee out-res/mapping-flac-ppea.log`  
`python mapping-save-data.py flac-pspe | tee out-res/mapping-flac-pspe.log`  
相関分析結果csvファイルの作成。

## sparcc

`sh clean-mkdir.sh`  
保存用ディレクトリを作成する(デフォルト30iter)。

`Rscript main.R | tee out-res/main.log`  
相関分析。

`python mapping-save-data.py | tee out-res/mapping.log`  
相関分析結果csvファイルの作成。  
