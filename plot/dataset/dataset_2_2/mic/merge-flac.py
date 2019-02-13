import pandas as pd
import numpy as np

head = 2
tail = 3

# データ読み込み
df_1_14 = pd.read_csv('flac-1-14.csv')
df_15_20 = pd.read_csv('flac-15-20.csv')

all_df = df_1_14

# 無駄なところを削除
# iter15-20
all_df.iloc[:, head+15:] = np.nan

# 残りをマッピング
# iter15-20
all_df.iloc[:, head+15:20+tail] = df_15_20.iloc[:, head+15:20+tail]

all_df.to_csv('../res-flac-mic.csv', index=False)
