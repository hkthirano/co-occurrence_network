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

method_list = ['sparcc', 'rebacca', 'spiec-easi', 'cclasso',
               'flac-pea', 'flac-spe', 'flac-ppea', 'flac-pspe', 'flac-mic']

# countデータの削除
df = df[df['calc-method'].isin(method_list)]



# 図１ メソッド比較図
df1 = df[(df['auc-type'] == 'prc') &
         (df['network'] == 'random') &
         (df['interact'] == 'random') &
         (df['s-max'] == 0.4) &
         (df['k-ave'] == 2) &
         (df['nn'] == 100) &
         (df['sampling'] == 500)]

#x1 = df1['calc-method'].fillna(0).tolist()
x1 = ['Pearson', 'Spearman', 'Partial\nPearson', 'Partial\nSpearman', 'MIC',
      'SparCC', 'REBACCA', 'SPIEC-EASI', 'CCLasso']
y1 = df1['mean'].fillna(0).tolist()
e1 = df1['SD'].fillna(0).tolist()

plt.bar(x1, y1, align='center', color=color, yerr=e1, ecolor='black')
plt.ylim([0, 1])
plt.xticks(rotation=45)

plt.title('ネットワーク構造:random | 相互作用:random | 種数:100 | 平均次数:2')
plt.ylabel('PRC-AUC')

plt.savefig('要旨画像/img1.png', bbox_inches='tight', dpi=300)
plt.close()



# 図１ 相互作用比較図
df2 = df[(df['auc-type'] == 'prc') &
         (df['network'] == 'random') &
         (df['calc-method'] == 'flac-pea') &
         (df['s-max'] == 0.4) &
         (df['k-ave'] == 2) &
         (df['nn'] == 100) &
         (df['sampling'] == 500)]

#x2 = df2['interact'].fillna(0).tolist()
x2 = ['ランダム', '協力', '混合', '競争', '拮抗']
y2 = df2['mean'].fillna(0).tolist()
e2 = df2['SD'].fillna(0).tolist()

plt.bar(x2, y2, align='center', color=color, yerr=e2, ecolor='black')
plt.ylim([0, 1])

#plt.xticks(rotation=45)

plt.title('推論手法:Pearson | ネットワーク構造:random | 種数:100 | 平均次数:2')
plt.ylabel('PRC-AUC')

plt.savefig('要旨画像/img2.png', bbox_inches='tight', dpi=300)
