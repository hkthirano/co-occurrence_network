import json
import itertools
import pandas as pd
import numpy as np


params = open("/Users/hirano/Sites/new-main/resource/params.json")
params = json.load(params)


# 組み合わせ作成
params_conbination = itertools.product(
                                       params['network'],
                                       params['interact'],
                                       params['s-max'],
                                       params['nn'],
                                       params['k-ave'],
                                       params['sampling'],
                                       params['ratio'])

params_conbination = pd.DataFrame( list(params_conbination) ,columns=['network', 'interact', 's-max', 'nn', 'k-ave', 'sampling', 'ratio'] )

# id列追加
id_list = [ id+1 for id in range(0, len(params_conbination.index)) ]
params_conbination['id'] = id_list

# 列入れ替え
col_list = ['id', 'network', 'interact', 's-max', 'nn', 'k-ave', 'sampling', 'ratio']
params_conbination = params_conbination.ix[:, col_list]

# ファイル名列追加
file_name_list = []
for i in range(0, len(params_conbination.index)):
    file_name = '{}-{}-{}-{}.txt'.format(int(params_conbination.iloc[i]['s-max']*100),
                                     params_conbination.iloc[i]['nn'],
                                     params_conbination.iloc[i]['k-ave'],
                                     params_conbination.iloc[i]['sampling'])
    file_name_list.append(file_name)
params_conbination['file-name'] = file_name_list

'''
# method列追加
method_res_tmp = [np.nan for i in range(len(id_list))]
for res_type in params['res-type']:
    for method in params['calc-method']:
        col_name = res_type + '-' + method
        params_conbination[col_name] = method_res_tmp
'''

# 保存
params_conbination.to_csv("resource/params-all.csv", index=False)

print(params_conbination.columns)

# make-data用に、samplingが最大の行だけ抽出して保存
sampling_max = max(params['sampling'])

sampling_max_params_conbination = params_conbination[params_conbination['sampling'] == sampling_max]

sampling_max_params_conbination.to_csv("resource/tmp/params-max-sampling.csv", index=False)

# 相関行列計算時のiter毎の結果保存用ファイル
id = params_conbination['id']
auc_type = params['auc-type']
method = params['calc-method']

params_for_res = itertools.product(id, auc_type, method)
params_for_res = pd.DataFrame( list(params_for_res) ,columns=['id', 'auc-type', 'calc-method'] )

# iter保存列を追加
iter_res_tmp = [np.nan for i in range(len(params_for_res))]
for iter in range(0, params['iter-num']):
    col_name = 'iter-{}'.format(iter+1)
    params_for_res[col_name] = np.nan

# nan-num・平均・分散・標準偏差の列を追加
params_for_res['nan-num'] = np.nan
params_for_res['mean'] = np.nan
params_for_res['variance'] = np.nan
params_for_res['SD'] = np.nan

# 保存
params_for_res.to_csv("resource/params-for-res.csv", index=False)
