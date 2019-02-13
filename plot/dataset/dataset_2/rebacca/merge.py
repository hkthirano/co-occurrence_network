import pandas as pd
import numpy as np

head = 2
tail = 3

# データ読み込み
df_1_12__26_27 = pd.read_csv('1-12_26-27.csv')
df_13__20_24 = pd.read_csv('13_20-24.csv')
df_14_19 = pd.read_csv('14-19.csv')
df_25 = pd.read_csv('25.csv')
df_28_30 = pd.read_csv('28-30.csv')

all_df = df_28_30

# 無駄なところを削除
# iter1-27
all_df.iloc[:, head+1:27+tail] = np.nan

# 残りをマッピング
# iter1-12
all_df.iloc[:, head+1:12+tail] = df_1_12__26_27.iloc[:, head+1:12+tail]
# iter26-27
all_df.iloc[:, head+26:27+tail] = df_1_12__26_27.iloc[:, head+26:27+tail]

# iter13
all_df.iloc[:, head+13] = df_13__20_24.iloc[:, head+13]
# iter20-24
all_df.iloc[:, head+20:24+tail] = df_13__20_24.iloc[:, head+20:24+tail]

# iter14-19
all_df.iloc[:, head+14:19+tail] = df_14_19.iloc[:, head+14:19+tail]

# iter25
all_df.iloc[:, head+25] = df_25.iloc[:, head+25]

all_df.to_csv('../res-rebacca.csv', index=False)
