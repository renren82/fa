import os
import datetime
import math
import pandas as pd
import numpy as np

path = "H:/"

ts_code_str = '002403.SZ'
path_root = 'H:/'
path_file = path_root + ts_code_str + '.xlsx'

df = pd.read_excel(path_file, sheet_name='history')

# null str is ‘nan'
# df['name'] = df['name'].apply(lambda x: str(x))
# for i in df.index.values:
#     # print(type(df.loc[i, 'name']))
#     if type(df.loc[i, 'name']) == str and df.loc[i, 'name'] != 'nan':
#         print(df.loc[i, 'name'])

# empty float
# for i in df.index.values:
#     # print(type(df.loc[i, 'ts_code']))
#     if type(df.loc[i, 'ts_code']) == float and df.loc[i, 'ts_code'] is np.nan:
#         print(df.loc[i, 'ts_code'])

# empty float64
# for i in df.index.values:
#     #　print(type(df.loc[i, 'trade_date']))　
#     if type(df.loc[i, 'trade_date']) == np.float64 and math.isnan(df.loc[i, 'trade_date']) is True:
#         print(df.loc[i, 'trade_date'])

# empty datetime
df['trade_date'] = pd.to_datetime(df['trade_date'], format="%Y%m%d")
# print(df.dtypes)
for i in df.index.values:
    # print(type(df.loc[i, 'trade_date']))
    if pd.isna(df.loc[i, 'trade_date']) is not True:
        print(df.loc[i, 'trade_date'])