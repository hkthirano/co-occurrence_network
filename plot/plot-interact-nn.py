import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os



# データの読み込み
df = pd.read_csv('dataset/dataset-all.csv')

f = open('dataset/dataset_1/params.json', 'r')
json = json.load(f)

network_list = json['network']
interact_list = json['interact']
method_list = ['sparcc', 'rebacca', 'spiec-easi', 'cclasso',
               'flac-pea', 'flac-spe', 'flac-ppea', 'flac-pspe', 'flac-mic']
smax_list = [0.3, 0.4, 0.5]
kave_list = [2, 4, 6, 8]
nn_list = json['nn']
sampling_list = [100, 300, 500]



# 表示関数

def show(df, auc_type, network, method, smax, kave, sampling, dir_path):
    
    d_use = df[(df['auc-type'] == auc_type) &
               (df['network'] == network) &
               (df['calc-method'] == method) &
               (df['s-max'] == smax) &
               (df['k-ave'] == kave) &
               (df['sampling'] == sampling)]

    for interact in interact_list:
        x = d_use.loc[d_use['interact'] == interact, 'nn'].unique()
        y = d_use.loc[d_use['interact'] == interact, 'mean']

        plt.plot(x, y, label=interact, marker="o", markersize=2)
        plt.legend(bbox_to_anchor=(1, 0), loc='lower right', borderaxespad=1, fontsize=8)
    
    if auc_type == 'roc':
        plt.ylim([0.4,1])
    elif auc_type == 'prc':
        plt.ylim([-0.01,1])
    
    plt.xlim([0, np.max(x)*1.05])

    plt.title('method:{} \nnetwork:{} | smax:{} | kave:{} | sampling:{} | \nnn:{}'.format(method, network, smax, kave, sampling, x))

    plt.xlabel('nn')
    plt.ylabel('{}-auc'.format(auc_type))

    plt.savefig('{}/sx{}-k{}-sp{}.png'.format(dir_path, smax, kave, sampling))
    plt.close()



# === メイン ===

for network in network_list:
    for method in method_list:

        # 途中結果
        print('=== {} - {} ==='.format(network, method))

        # 保存用ディレクトリ作成
        dir_path = 'img/show-interact-nn/st-{}/{}'.format(network, method)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        for smax in smax_list:
            for kave in kave_list:
                for sampling in sampling_list:

                    #show(df, 'roc', network, method, smax, kave, sampling, dir_path)

                    show(df, 'prc', network, method, smax, kave, sampling, dir_path)