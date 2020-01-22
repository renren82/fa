import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path_root = 'P:/project/python/Fn/'
path_file = path_root + '000559.SZ_result.xlsx'

df = pd.read_excel(path_file, sheet_name='history', converters={'signal_date': str})

df['signal_date'] = pd.to_datetime(df['signal_date'])
# x = df.loc[:, 'signal_date'].values
#
# y = df.loc[:, 'delta_%'].values


df = df.set_index('signal_date')
# print(df.index)

df['delta_%'].plot()
df['high_%'].plot()

plt.grid(True)
plt.ylabel('%', size=15)
plt.title('title name')
# plt.rcParams['savefig.dpi'] = 1024
plt.show()
# plt.savefig('./a.png', dpi=1000)
# plt.savefig('./a.png')
