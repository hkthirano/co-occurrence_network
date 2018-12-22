import json
import itertools
import pandas as pd
import numpy as np



# 下準備
json_path = open("/Users/hirano/Sites/new-main/resource/params.json")
j_data = json.load(json_path)

iter_num = j_data['iter-num']

# 保存用ファイルを読み込んでgeneralだけを抽出する
df = pd.read_csv(j_data['params-for-res-csv'])
df_save = df[(df['calc-method'] == 'count-pea') |
             (df['calc-method'] == 'count-spe') |
             (df['calc-method'] == 'count-ppea') |
             (df['calc-method'] == 'count-pspe') |
             (df['calc-method'] == 'flac-pea') |
             (df['calc-method'] == 'flac-spe') |
             (df['calc-method'] == 'flac-ppea') |
             (df['calc-method'] == 'flac-pspe')]

# 基準paramsの読み込み
params = pd.read_csv(j_data['params-all-csv'])

# paramsに従って、１行ずつaucをマッピングしていく
for i in range(len(params)):
    id = params.iloc[i]['id']

    for iter in range(1, iter_num + 1):

        # @@@@@ 1 count-pea @@@@@
        auc_file_1 = 'out-res/iter-{}/id-{}-count-pea.txt'.format(iter, id)
        try:
            auc_1 = np.loadtxt(auc_file_1)
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'count-pea') & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc_1[0]
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'count-pea') & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc_1[1]
        except:
            print('\n\n', auc_file_1, ' ない\n\n')

        # @@@@@ 2 count-spe @@@@@
        auc_file_2 = 'out-res/iter-{}/id-{}-count-spe.txt'.format(iter, id)
        try:
            auc_2 = np.loadtxt(auc_file_2)
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'count-spe') & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc_2[0]
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'count-spe') & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc_2[1]
        except:
            print('\n\n', auc_file_2, ' ない\n\n')

        # @@@@@ 3 count-ppea @@@@@
        auc_file_3 = 'out-res/iter-{}/id-{}-count-ppea.txt'.format(iter, id)
        try:
            auc_3 = np.loadtxt(auc_file_3)
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'count-ppea') & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc_3[0]
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'count-ppea') & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc_3[1]
        except:
            print('\n\n', auc_file_3, ' ない\n\n')

        # @@@@@ 4 count-pspe @@@@@
        auc_file_4 = 'out-res/iter-{}/id-{}-count-pspe.txt'.format(iter, id)
        try:
            auc_4 = np.loadtxt(auc_file_4)
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'count-pspe') & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc_4[0]
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'count-pspe') & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc_4[1]
        except:
            print('\n\n', auc_file_4, ' ない\n\n')

        # @@@@@ 5 flac-pea @@@@@
        auc_file_5 = 'out-res/iter-{}/id-{}-flac-pea.txt'.format(iter, id)
        try:
            auc_5 = np.loadtxt(auc_file_5)
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'flac-pea') & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc_5[0]
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'flac-pea') & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc_5[1]
        except:
            print('\n\n', auc_file_5, ' ない\n\n')

        # @@@@@ 6 flac-spe @@@@@
        auc_file_6 = 'out-res/iter-{}/id-{}-flac-spe.txt'.format(iter, id)
        try:
            auc_6 = np.loadtxt(auc_file_6)
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'flac-spe') & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc_6[0]
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'flac-spe') & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc_6[1]
        except:
            print('\n\n', auc_file_6, ' ない\n\n')
        
        # @@@@@ 7 flac-ppea @@@@@
        auc_file_7 = 'out-res/iter-{}/id-{}-flac-ppea.txt'.format(iter, id)
        try:
            auc_7 = np.loadtxt(auc_file_7)
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'flac-ppea') & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc_7[0]
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'flac-ppea') & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc_7[1]
        except:
            print('\n\n', auc_file_7, ' ない\n\n')
        
        # @@@@@ 8 flac-pspe @@@@@
        auc_file_8 = 'out-res/iter-{}/id-{}-flac-pspe.txt'.format(iter, id)
        try:
            auc_8 = np.loadtxt(auc_file_8)
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'flac-pspe') & (df_save['auc-type'] == 'roc'), 'iter-{}'.format(iter)] = auc_8[0]
            df_save.loc[(df_save['id'] == id) & (df_save['calc-method'] == 'flac-pspe') & (df_save['auc-type'] == 'prc'), 'iter-{}'.format(iter)] = auc_8[1]
        except:
            print('\n\n', auc_file_8, ' ない\n\n')

# 保存
df_save.to_csv('res-general.csv', index=False)
        


