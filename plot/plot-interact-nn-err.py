import pandas as pd
import matplotlib.pyplot as plt
import json
import os



color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
color = color_list[0:5]



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



# 表示関数

def show(df, auc_type, network, method, smax, kave, nn, sampling, dir_path):
    
    d_use = df[(df['auc-type'] == auc_type) &
               (df['network'] == network) &
               (df['calc-method'] == method) &
               (df['s-max'] == smax) &
               (df['k-ave'] == kave) &
               (df['nn'] == nn) &
               (df['sampling'] == sampling)]

    
    x = d_use['interact'].fillna(0).tolist()
    y = d_use['mean'].fillna(0).tolist()
    e = d_use['SD'].fillna(0).tolist()

    #swp_x = [x[COMPT], x[RANDOM], x[PP], x[MIX], x[MUTUAL]]
    #swp_y = [y[COMPT], y[RANDOM], y[PP], y[MIX], y[MUTUAL]]
    #swp_e = [e[COMPT], e[RANDOM], e[PP], e[MIX], e[MUTUAL]]
    #swp_color = [color[COMPT], color[RANDOM], color[PP], color[MIX], color[MUTUAL]]

    #plt.bar(swp_x, swp_y, align = "center", color=swp_color, yerr=swp_e, ecolor = "black")
    plt.bar(x, y, align = "center", color=color, yerr=e, ecolor = "black")
    plt.ylim([0, 1])

    plt.title('method:{} \nnetwork:{} | smax:{} | kave:{} | nn:{} | sampling:{}'.format(method, network, smax, kave, nn, sampling))
    plt.ylabel('{}-auc'.format(auc_type))

    plt.savefig('{}/sx{}-k{}-n{}-sp{}.png'.format(dir_path, smax, kave, nn, sampling))
    
    plt.close()



# === メイン ===

for network in network_list:
    for method in method_list:

        # 途中結果
        print('=== {} - {} ==='.format(network, method))

        # 保存用ディレクトリ作成
        dir_path = 'img/show-interact-nn-err/st-{}/{}'.format(network, method)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        for smax in smax_list:
            for kave in kave_list:
                for nn in nn_list:
                    for sampling in sampling_list:

                        show(df, 'roc', network, method, smax, kave, nn, sampling, dir_path)

                        show(df, 'prc', network, method, smax, kave, nn, sampling, dir_path)