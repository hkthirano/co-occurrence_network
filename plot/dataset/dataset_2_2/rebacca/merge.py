import pandas as pd
import numpy as np

head = 2
tail = 3

# データ読み込み
df_1_12 = pd.read_csv('1-12.csv')
df_13_16 = pd.read_csv('13-16.csv')
df_17_20 = pd.read_csv('17-20.csv')

all_df = df_1_12

# 無駄なところを削除
# iter13-20
all_df.iloc[:, head+13:20+tail] = np.nan

# 残りをマッピング
# iter13-16
all_df.iloc[:, head+13:16+tail] = df_13_16.iloc[:, head+13:16+tail]

# iter17-20
all_df.iloc[:, head+17:20+tail] = df_17_20.iloc[:, head+17:20+tail]

all_df.to_csv('../res-rebacca.csv', index=False)
