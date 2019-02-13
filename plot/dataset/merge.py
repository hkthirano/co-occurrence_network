import pandas as pd 
import numpy as np
import json
import os



# jsonの読み込み
json_1 = open('dataset_1/params.json', 'r')
json_2 = open('dataset_2/params.json', 'r')
json_1_2 = open('dataset_1_2/params.json', 'r')
json_2_2 = open('dataset_2_2/params.json', 'r')

j_1 = json.load(json_1)
j_2 = json.load(json_2)
j_1_2 = json.load(json_1_2)
j_2_2 = json.load(json_2_2)

# 基準params.csvの読み込み
params_1 = pd.read_csv('dataset_1/params-all.csv')
params_2 = pd.read_csv('dataset_2/params-all.csv')



### dataset_1系の準備
# dataset_1を縦にマージ
df_1_list = []
for method in j_1['calc-method']:
    res_1 = pd.read_csv('dataset_1/res-{}.csv'.format(method))
    df_1_list.append(res_1)

df_1_concat = df_1_list[0]
for i in range(1, len(df_1_list)):
    df_1_concat = pd.concat([df_1_concat, df_1_list[i]])

# dataset_1_2を縦にマージ
df_1_2_list = []
for method in j_1_2['calc-method']:
    res_1_2 = pd.read_csv('dataset_1_2/res-{}.csv'.format(method))
    df_1_2_list.append(res_1_2)

df_1_2_concat = df_1_2_list[0]
for i in range(1, len(df_1_2_list)):
    df_1_2_concat = pd.concat([df_1_2_concat, df_1_2_list[i]])

# dataset_1にdataset_1_2の+20iterを追加（横にマージ）
df_1_concat = df_1_concat.drop(['nan-num', 'mean', 'variance', 'SD'], axis=1)
df_1_2_concat = df_1_2_concat.drop(['id', 'auc-type', 'calc-method'], axis=1)

df_1_2_col_name = ['iter-{}'.format(i) for i in range(31, 51)]
df_1_2_col_name.extend(['nan-num', 'mean', 'variance', 'SD'])
df_1_2_concat.columns = df_1_2_col_name

df_1_all = pd.concat([df_1_concat, df_1_2_concat], axis=1)

# dataset_1系とparams_1を横にマージ
df_1_all = pd.merge(df_1_all, params_1, how='left')



### dataset_2系の準備
# dataset_2を縦にマージ
df_2_list = []
for method in j_2['calc-method']:
    res_2 = pd.read_csv('dataset_2/res-{}.csv'.format(method))
    df_2_list.append(res_2)

df_2_concat = df_2_list[0]
for i in range(1, len(df_2_list)):
    df_2_concat = pd.concat([df_2_concat, df_2_list[i]])

# dataset_2_2を縦にマージ
df_2_2_list = []
for method in j_2_2['calc-method']:
    res_2_2 = pd.read_csv('dataset_2_2/res-{}.csv'.format(method))
    df_2_2_list.append(res_2_2)

df_2_2_concat = df_2_2_list[0]
for i in range(1, len(df_2_2_list)):
    df_2_2_concat = pd.concat([df_2_2_concat, df_2_2_list[i]])

# dataset_2にdataset_2_2の+20iterを追加（横にマージ）
df_2_concat = df_2_concat.drop(['nan-num', 'mean', 'variance', 'SD'], axis=1)
df_2_2_concat = df_2_2_concat.drop(['id', 'auc-type', 'calc-method'], axis=1)

df_2_2_col_name = ['iter-{}'.format(i) for i in range(31, 51)]
df_2_2_col_name.extend(['nan-num', 'mean', 'variance', 'SD'])
df_2_2_concat.columns = df_2_2_col_name

df_2_all = pd.concat([df_2_concat, df_2_2_concat], axis=1)

# dataset_2系とparams_2を横にマージ
df_2_all = pd.merge(df_2_all, params_2, how='left')



### dataset_1系とdataset_2系を縦にマージ
df_all = pd.concat([df_1_all, df_2_all])



### 前処理
# 3~53 : iter1~iter50

# 行毎に欠損値の数を取得
df_all.loc[:, 'nan-num'] = df_all.iloc[:, 3:53].isnull().sum(axis=1)

# 欠損値以外の平均を計算
df_all.loc[:, 'mean'] = np.nanmean(df_all.iloc[:, 3:53], axis=1)

# 欠損値以外の不偏標準偏差を計算
df_all.loc[:, 'SD'] = np.nanstd(df_all.iloc[:, 3:53], axis=1)



df_all.to_csv('dataset-all.csv', index=False)
