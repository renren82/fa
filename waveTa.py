import os
import datetime
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
title_name = 'zgzg'
# .SH .SZ '002403.SZ'
ts_code_str = '601989.SH'
st_code_str = '601989'
path_root = 'H:/'
path_file = path_root + ts_code_str + '.xlsx'
# path_result_file = path_root + ts_code_str + '_result' + '.xlsx'

show_num = 233

dt_now = datetime.datetime.now().date()
# dt_now = datetime.datetime.strptime('20160101', '%Y%m%d').date()
dt_now_str = dt_now.strftime('%Y%m%d')
dt_data_start = dt_now - datetime.timedelta(days=800)
dt_data_start_str = dt_data_start.strftime('%Y%m%d')


def file_exist(path):
    if os.path.exists(path):
        return 1
    else:
        return 0


def get_ta_data(path_data):
    """
    get base delta value for ma3-ma5
    """
    # if os.path.exists(path_data):
    #     return 1

    # asset	str	Y	资产类别：E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 CB可转债（v1.2.39），默认E
    df = ts.pro_bar(ts_code=ts_code_str, adj='qfq', start_date=dt_data_start_str,
                    end_date=dt_now_str, freq='D', ma=[3, 5, 8, 13, 21, 34, 55, 89, 144, 233])
    # print(df.head())
    df['delta'] = df['ma3'] - df['ma5']

    writer = pd.ExcelWriter(path_data)
    # print(type(df).__name__)
    if type(df).__name__ == 'DataFrame':
        df.to_excel(writer, sheet_name='history', index=False)
        writer.save()


def compute_power_data(df_data, k_start, k_end):
    """
     compute mean surface
    """
    i = k_end
    delta_sum = 0
    while i != k_start:
        delta_sum += df_data.loc[i, 'ma3'] - df_data.loc[i, 'ma5']
        df_data.loc[i, 'power'] = float(delta_sum / (k_end - i+1))
        # df_data.loc[i, 'power'] = float(delta_sum)
        i -= 1
    return 0


get_ta_data(path_file)
df = pd.read_excel(path_file, sheet_name='history', converters={'trade_date': str})

k_start = -1
k_end = 0
k = 0
for k in df.index.values:
    if ((df.loc[k, 'ma3'] >= df.loc[k, 'ma5']) and (df.loc[k+1, 'ma3'] < df.loc[k+1, 'ma5'])) or ((df.loc[k, 'ma3'] <= df.loc[k, 'ma5']) and (df.loc[k+1, 'ma3'] > df.loc[k+1, 'ma5'])):
        k_end = k
        compute_power_data(df, k_start, k_end)
        k_start = k_end

# df['delta'] = df['ma3'] - df['ma5']
# df['close_%'] = df['close']/7.5 - 1

# writer = pd.ExcelWriter(path_result_file)
# df.to_excel(writer, sheet_name='history', index=False)
# writer.save()

# df['trade_date'] = pd.to_datetime(df['trade_date'])
# # x = df.loc[:, 'signal_date'].values
# #
# # y = df.loc[:, 'delta_%'].values
#
# df = df.set_index('trade_date')

max_index = max(df.index.values)

plt.subplot(211)
df[0:show_num]['delta'].plot()
# df['power'].plot(kind='bar', color='r')
df[0:show_num]['power'].plot()
# df['close_%'].plot()

#                   记号形状       颜色           点的大小    设置标签
# plt.scatter(x, y, marker = 'x',color = 'red', s = 40 ,label = 'First')

# plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5), arrowprops=dict(facecolor='black', shrink=0.05),)
# plt.text(0.5, 1, 'put some text')

plt.grid(True)
plt.ylabel('power', size=15)
plt.gca().invert_xaxis()
plt.legend()
plt.title(title_name)

plt.subplot(212)
# df[10:].close.plot()
df[0:show_num]['close'].plot()

plt.grid(True)
plt.ylabel('close', size=15)
# plt.title(title_name)
# plt.rcParams['savefig.dpi'] = 1024
plt.gca().invert_xaxis()
plt.legend()
plt.show()
# plt.savefig('./a.png', dpi=1000)
# plt.savefig('./a.png')


