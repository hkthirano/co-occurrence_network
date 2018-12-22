import json
import itertools
import pandas as pd
import numpy as np



# 下準備
json_path = open("/Users/hirano/Sites/new-main/resource/params.json")
j_data = json.load(json_path)

iter_num = j_data['iter-num']

# 保存用ファイルを読み込んでmicだけを抽出する
df = pd.read_csv(j_data['params-for-res-csv'])
df_save = df[(df['calc-method'] == 'count-mic') | (df['calc-method'] == 'flac-mic')]

# 基準paramsの読み込み
params = pd.read_csv(j_data['params-all-csv'])

# paramsに従って、１行ずつaucをマッピングしていく
for i in range(len(params)):
    id = params.iloc[i]['id']

    for iter in range(1, iter_num + 1):
        # count
        auc_file_count = 'out-res/iter-{}/id-{}-count.txt'.format(iter, id)
        try:
            auc_count = np.loadtxt(auc_file_count)

            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'count-mic') & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc_count[0]

            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'count-mic') & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc_count[1]
        except:
            print('\n\n', auc_file_count, ' ない\n\n')

        # flac
        auc_file_flac = 'out-res/iter-{}/id-{}-flac.txt'.format(iter, id)
        try:
            auc_flac = np.loadtxt(auc_file_flac)

            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'flac-mic') & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc_flac[0]

            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'flac-mic') & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc_flac[1]
        except:
            print('\n\n', auc_file_flac, ' ない\n\n')


# 保存
df_save.to_csv('res-mic.csv', index=False)
        


