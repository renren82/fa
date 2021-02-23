import os
import datetime
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
上证50指数   sh000016
沪深300    sh000300
中证环保指数 sh000827
中证500  sh000905
上证指数   sh999999
深证成指   399001
中小板指   sz399005
创业板指 sz399006
"""

path_root = 'H:/'
# ts_code_str = 'sh000016_60min'
# ts_code_str = 'sh000016_d'
ts_code_str = 'sh000827_M'
path_file = path_root + ts_code_str + '.xlsx'
# for 60min
show_num = -300
# for 30min show_num = -450


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


def compute_back_power_data(df_data, k_start, k_end):
    """
     compute mean surface
    """
    i = k_end
    delta_sum = 0
    while i <= k_start:
        delta_sum += df_data.loc[i, 'ma3'] - df_data.loc[i, 'ma5']
        df_data.loc[i, 'power'] = float(delta_sum / (i - k_end + 1))
        # df_data.loc[i, 'power'] = float(delta_sum)
        i += 1
    return 0


def power_back_data(df):
    '''
    power from ma3 - ma5
    surface
    '''
    k_start = len(df.index.values) - 1
    k_end = 0
    k = len(df.index.values) - 1
    while k > 0:
        if ((df.loc[k, 'ma3'] >= df.loc[k, 'ma5']) and (df.loc[k - 1, 'ma3'] < df.loc[k - 1, 'ma5'])) or (
                (df.loc[k, 'ma3'] <= df.loc[k, 'ma5']) and (df.loc[k - 1, 'ma3'] > df.loc[k - 1, 'ma5'])):
            k_end = k
            compute_back_power_data(df, k_start, k_end)
            k_start = k_end
        k -= 1


def power_data(df):
    k_start = -1
    k_end = 0
    k = 0
    for k in df.index.values:
        if ((df.loc[k, 'ma3'] >= df.loc[k, 'ma5']) and (df.loc[k + 1, 'ma3'] < df.loc[k + 1, 'ma5'])) or (
                (df.loc[k, 'ma3'] <= df.loc[k, 'ma5']) and (df.loc[k + 1, 'ma3'] > df.loc[k + 1, 'ma5'])):
            k_end = k
            compute_power_data(df, k_start, k_end)
            k_start = k_end


# if __name__ == '__main__':
def main(ts_code):
    global ts_code_str, path_file
    ts_code_str = ts_code
    path_file = path_root + ts_code_str + '.xlsx'
    df = pd.read_excel(path_file)

    power_data(df)

    # df['delta'] = df['ma3'] - df['ma5']
    # df['close_%'] = df['close']/7.5 - 1

    writer = pd.ExcelWriter(path_file)
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()

    # df['trade_date'] = pd.to_datetime(df['trade_date'])
    # # x = df.loc[:, 'signal_date'].values
    # #
    # # y = df.loc[:, 'delta_%'].values
    #
    # df = df.set_index('trade_date')

    # max_index = max(df.index.values)
    #
    # plt.subplot(311)
    # df[show_num:]['delta'].plot()
    # # df['power'].plot(kind='bar', color='r')
    # df[show_num:]['power'].plot()
    # # df['close_%'].plot()
    #
    # #                   记号形状       颜色           点的大小    设置标签
    # # plt.scatter(x, y, marker = 'x',color = 'red', s = 40 ,label = 'First')
    #
    # # plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5), arrowprops=dict(facecolor='black', shrink=0.05),)
    # # plt.text(0.5, 1, 'put some text')
    #
    # plt.grid(True)
    # plt.ylabel('power', size=15)
    # plt.title(ts_code_str)
    # # plt.gca().invert_xaxis()
    # plt.legend()
    #
    # plt.subplot(312)
    # # df[10:].close.plot()
    # # df['close'].plot()
    # # df.close.plot()
    # df[show_num:]['close'].plot()
    #
    # plt.grid(True)
    # plt.ylabel('close', size=15)
    # # plt.title(ts_code_str)
    # # plt.rcParams['savefig.dpi'] = 1024
    # # plt.gca().invert_xaxis()
    # plt.legend()
    #
    # plt.subplot(313)
    # # df[10:].close.plot()
    # # df['close'].plot()
    # # df.close.plot()
    # df[show_num:]['ma_v_3'].plot(color='g')
    # plt.grid(True)
    # plt.ylabel('ma_v_3', size=15)
    # # plt.title('title name')
    # # plt.rcParams['savefig.dpi'] = 1024
    # # plt.gca().invert_xaxis()
    # plt.legend()
    #
    # plt.show()
    # # plt.savefig('./a.png', dpi=1000)
    # # plt.savefig('./a.png')
