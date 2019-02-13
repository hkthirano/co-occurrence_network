import pandas as pd
import matplotlib.pyplot as plt
import json
import os



color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
color = color_list[0:10]# + color_list[0:5]

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
nn_list = [20, 50, 100]
sampling_list = [100, 300, 500]

# countデータの削除
df = df[df['calc-method'].isin(method_list)]


# 表示関数

def show(df, auc_type, network, interact, smax, kave, nn, sampling, dir_path):
    
    d_use = df[(df['auc-type'] == auc_type) &
               (df['network'] == network) &
               (df['interact'] == interact) &
               (df['s-max'] == smax) &
               (df['k-ave'] == kave) &
               (df['nn'] == nn) &
               (df['sampling'] == sampling)]

    
    x = d_use['calc-method'].fillna(0).tolist()
    y = d_use['mean'].fillna(0).tolist()
    e = d_use['SD'].fillna(0).tolist()

    plt.bar(x, y, align = "center", color=color, yerr=e, ecolor = "black")
    plt.ylim([0, 1])

    plt.xticks(rotation=45)

    plt.title('network:{} | interact:{} \nsmax:{} | kave:{} | nn:{} | sampling:{}'.format(network, interact, smax, kave, nn, sampling))
    plt.ylabel('{}-auc'.format(auc_type))

    plt.savefig('{}/sx{}-k{}-n{}-sp{}.png'.format(dir_path, smax, kave, nn, sampling), bbox_inches='tight')
    
    plt.close()



# === メイン ===

for network in network_list:
    for interact in interact_list:

        # 途中結果
        print('=== {} - {} ==='.format(network, interact))

        # 保存用ディレクトリ作成
        dir_path = 'img/show-method-nn-err/st-{}/in-{}'.format(network, interact)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        for smax in smax_list:
            for kave in kave_list:
                for nn in nn_list:
                    for sampling in sampling_list:

                        #show(df, 'roc', network, interact, smax, kave, nn, sampling, dir_path)

                        show(df, 'prc', network, interact, smax, kave, nn, sampling, dir_path)