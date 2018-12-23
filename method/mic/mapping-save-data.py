import json
import itertools
import pandas as pd
import numpy as np
import sys



# 下準備
json_path = open("/Users/hirano/Sites/new-main/resource/params.json")
j_data = json.load(json_path)

iter_num = j_data['iter-num']

# 保存用ファイルを読み込んでmicだけを抽出する
df = pd.read_csv(j_data['params-for-res-csv'])
df_save = df[(df['calc-method'] == 'count-mic') | (df['calc-method'] == 'flac-mic')]

# 基準paramsの読み込み
params = pd.read_csv(j_data['params-all-csv'])

# メソッド種類
args = sys.argv
method = args[1]



# paramsに従って、１行ずつaucをマッピングしていく
for i in range(len(params)):
    id = params.iloc[i]['id']

    for iter in range(1, iter_num + 1):
        auc_file = 'out-res/iter-{}/id-{}-{}.txt'.format(iter, id, method)

        try:
            auc = np.loadtxt(auc_file)

            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == method) & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc[0]

            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == method) & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc[1]
        except:
            print('\n\n', auc_file, ' ない\n\n')

# 保存
df_save.to_csv('res-{}.csv'.format(method), index=False)