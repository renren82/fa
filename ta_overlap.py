import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import talib as ta
import tushare as ts

# %matplotlib inline

# 正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


def df_to_excel(path_data, df_data):
    if os.path.exists(path_data):
        return 1

    writer = pd.ExcelWriter(path_data)
    # print(type(df).__name__)
    if type(df_data).__name__ == 'DataFrame':
        df_data.to_excel(writer, sheet_name='sheet1', index=True)
        writer.save()

# print(ta.get_functions())
# print(ta.get_function_groups())

ta_fun = ta.get_function_groups()
ta_fun.keys()


df = ts.get_k_data('sh', start='2000-01-01')
print(df.head())
df.index = pd.to_datetime(df.date)
df = df.sort_index()

types = ['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA', 'MAMA', 'T3']
df_ma = pd.DataFrame(df.close)
for i in range(len(types)):
    df_ma[types[i]] = ta.MA(df.close, timeperiod=5, matype=i)
# print(df_ma.tail())
df_to_excel('ma.xlsx', df_ma)
df_ma.loc['2018-08-01':].plot(figsize=(16, 6))
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.title('上证指数各种类型移动平均线',fontsize=15)
plt.xlabel('')
plt.show()

# 画5、30、120、250指数移动平均线
N = [5,30,120,250]
for i in N:
    df['ma_'+str(i)] = ta.EMA(df.close,timeperiod=i)
df.tail()

df.loc['2014-01-01':, ['close','ma_5','ma_30','ma_120','ma_250']].plot(figsize=(16,6))
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.title('上证指数走势', fontsize=15)
plt.xlabel('')
plt.show()

H_line, M_line, L_line = ta.BBANDS(df.close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
df1 = pd.DataFrame(df.close, index=df.index, columns=['close'])
df1['H_line'] = H_line
df1['M_line'] = M_line
df1['L_line'] = L_line
df1.tail()


df1.loc['2013-01-01':'2014-12-30'].plot(figsize=(16,6))
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.title('上证指数布林线', fontsize=15)
plt.xlabel('')
plt.show()


df2=pd.DataFrame(df.close)
df2['HT'] = ta.HT_TRENDLINE(df.close)
periods = np.array([3]*len(df), dtype=float)
df2['MAVP'] = ta. MAVP(df.close,periods)
df2['MIDPOINT'] = ta.MIDPOINT(df.close)
df2['MIDPRICE'] = ta.MIDPRICE(df.high,df.low)
df2['SAR'] = ta.SAR(df.high,df.low)
df2['SAREXT'] = ta.SAREXT(df.high,df.low)
df2.tail()

df2.loc['2018-01-01':'2019-02-21', ['close', 'HT', 'MAVP', 'MIDPOINT', 'MIDPRICE', 'SAR']].plot(figsize=(16,6))
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.title('上证指数的其他趋势指标线', fontsize=15)
plt.xlabel('')
plt.show()


df2.loc['2018-01-01':'2019-02-21','SAREXT'].plot(figsize=(16,6))
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.title('上证指数的抛物线扩展走势',fontsize=15)
plt.xlabel('')
plt.show()