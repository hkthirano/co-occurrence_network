import pandas as pd
import numpy as np

head = 2
tail = 3

# データ読み込み
df_1_14 = pd.read_csv('count-1-20.csv')
df_21_25 = pd.read_csv('count-21-25.csv')
df_26_30 = pd.read_csv('count-26-30.csv')

all_df = df_1_14

# 無駄なところを削除
# iter21-30
all_df.iloc[:, head+21:] = np.nan

# 残りをマッピング
# iter21-25
all_df.iloc[:, head+21:25+tail] = df_21_25.iloc[:, head+21:25+tail]
# iter26-30
all_df.iloc[:, head+26:30+tail] = df_26_30.iloc[:, head+26:30+tail]

all_df.to_csv('../res-count-mic.csv', index=False)
