import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os



color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
color = color_list[0:5]

line_list = ['-', ':', '--']



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

def show(df, auc_type, interact, method, smax, kave, sampling, dir_path):
    
    d_use = df[(df['interact'] == interact) &
               (df['auc-type'] == auc_type) &
               (df['calc-method'] == method) &
               (df['s-max'] == smax) &
               (df['k-ave'] == kave) &
               (df['sampling'] == sampling)]

    for i, network in enumerate(network_list):
        x = d_use.loc[(d_use['network'] == network), 'nn'].unique()
        y = d_use.loc[(d_use['network'] == network), 'mean']

        plt.plot(x, y, label='{}'.format(network), marker="o", markersize=2, linestyle=line_list[i], color=color[i])
        plt.legend(bbox_to_anchor=(1, 0), loc='lower right', borderaxespad=1, fontsize=8)
    
    if auc_type == 'roc':
        plt.ylim([0.4,1])
    elif auc_type == 'prc':
        plt.ylim([-0.01,1])
    
    plt.xlim([0, np.max(x)*1.05])

    plt.title('method:{} | interact:{}\nsmax:{} | kave:{} | sampling:{} | \nnn:{}'.format(method, interact, smax, kave, sampling, x))

    plt.xlabel('nn')
    plt.ylabel('{}-auc'.format(auc_type))

    plt.savefig('{}/sx{}-k{}-sp{}.png'.format(dir_path, smax, kave, sampling))
    plt.close()



# === メイン ===

for interact in interact_list:
    print('=== {} ==='.format(interact))
    for method in method_list:

        # 途中結果

        print('\t=== {} ==='.format(method))

        # 保存用ディレクトリ作成
        dir_path = 'img/show-network-nn/in-{}/{}'.format(interact, method)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        for smax in smax_list:
            for kave in kave_list:
                for sampling in sampling_list:

                    show(df, 'prc', interact, method, smax, kave, sampling, dir_path)