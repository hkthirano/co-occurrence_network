import json
import itertools
import pandas as pd
import numpy as np



# 下準備
json_path = open("/Users/hirano/Sites/new-main/resource/params.json")
j_data = json.load(json_path)

iter_num = j_data['iter-num']

# 保存用ファイルを読み込んでspiec-easiだけを抽出する
df = pd.read_csv(j_data['params-for-res-csv'])
df_save = df[df['calc-method'] == 'spiec-easi']

# 基準paramsの読み込み
params = pd.read_csv(j_data['params-all-csv'])

# paramsに従って、１行ずつaucをマッピングしていく
for i in range(len(params)):
    id = params.iloc[i]['id']

    for iter in range(1, iter_num + 1):
        
        auc_file = 'out-res/iter-{}/id-{}.txt'.format(iter, id)
        try:
            auc = np.loadtxt(auc_file)

            df_save.loc[(df_save['id'] == id) & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc[0]

            df_save.loc[(df_save['id'] == id) & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc[1]
        except:
            print('\n\n', auc_file, ' ない\n\n')

# 保存
df_save.to_csv('res-spiec-easi.csv', index=False)
        


