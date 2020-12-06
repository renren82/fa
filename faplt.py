import os
import datetime
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
title_name = 'wxqc'
# .SH .SZ '002403.SZ'
ts_code_str = '000559.SZ'
st_code_str = '000559'
path_root = 'H:/'
path_file = path_root + ts_code_str + '.xlsx'
# path_result_file = path_root + ts_code_str + '_result' + '.xlsx'

show_num = 233

dt_now = datetime.datetime.now().date()
# dt_now = datetime.datetime.strptime('20160101', '%Y%m%d').date()
dt_now_str = dt_now.strftime('%Y%m%d')
dt_data_start = dt_now - datetime.timedelta(days=800)
dt_data_start_str = dt_data_start.strftime('%Y%m%d')


def main(code_str, show_start):
    global ts_code_str, path_file, show_num, title_name
    ts_code_str = code_str
    title_name = code_str
    path_file = path_root + ts_code_str + '.xlsx'
    df = pd.read_excel(path_file, sheet_name='Sheet1', converters={'trade_date': str})

    show_num = 0
    for k in df.index.values:
        show_num += 1
        if df.loc[k, 'trade_date'] == show_start:
            break

    fig, ax = plt.subplots(1, 1)
    # 共享x轴，生成次坐标轴
    ax_sub = ax.twinx()
    # 绘图
    l1, = ax.plot(df.index[0:show_num], df.close[0:show_num], 'g-', label='close')
    l2, = ax_sub.plot(df.index[0:show_num], df.delta[0:show_num], 'r-', label='delta')
    # l3, = ax_sub.plot(df.index[0:show_num], df.power[0:show_num], 'b-', label='power')
    plt.gca().invert_xaxis()
    # 放置图例
    # plt.legend(handles=[l1, l2, l3], labels=['close', 'delta', 'power'], loc=0)
    # plt.legend(handles=[l1, l2], labels=['close', 'delta'], loc=0)
    plt.legend(handles=[l1, l2], labels=['close', 'delta'], loc='upper left')
    # 设置主次y轴的title
    ax.set_ylabel('close')
    ax_sub.set_ylabel('delta')
    # 设置x轴title
    ax.set_xlabel('index')
    # 设置图片title
    ax.set_title(title_name)
    plt.grid(True)
    plt.show()
