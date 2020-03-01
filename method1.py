import tushare as ts
import os
import datetime
import numpy as np
# import talib
import pandas as pd
from playsound import playsound



# set parameter

resultpath = 'H:/'
filedownloadpath = 'H:/SSE/'


data = pd.read_excel(filedownloadpath + 'list.xlsx')

new_pd = []
low_all_ma_flag = 1

def method1(filespath):
    # for root, dirs, files in os.walk(filespath):
    #
    #     # root 表示当前正在访问的文件夹路径
    #     # dirs 表示该文件夹下的子目录名list
    #     # files 表示该文件夹下的文件list
    #
    #     # 遍历文件
    #     for f in files:
    #         print(os.path.join(root, f))
    global  low_all_ma_flag
    # converters={'wenti':str}
    df_data = pd.read_excel(filespath, sheet_name='history')

    if 'high' not in list(df_data):
        return 0

    l_high = df_data.loc[:, 'high'].tolist()
    if l_high:
        # print(l_high.index(max(ll)))
        # print(l_high.index(min(ll)))
        max_index = l_high.index(max(l_high))
        print(max_index)
        max_value = float(max(l_high))
    else:
        return 0

    l_low = df_data.loc[:, 'low'].tolist()
    if l_low:
        # print(l_high.index(max(ll)))
        # print(l_high.index(min(ll)))
        min_index = l_low.index(min(l_low))
        min_value = float(min(l_low))
        ta_days = len(l_low)
    else:
        return 0

    per_value = (max_value - min_value) * 100 / min_value
    print(per_value)

    # near min_value
    now_position = abs(df_data.loc[0, 'low'] - min_value) * 100 / min_value

    # lower all ma
    day = 3
    while i < 801:
        ma_str = 'ma' + str(i)
        day += 1
        if ma_str in list(df_data):
            if df_data.loc[0, 'low'] > df_data.loc[0, ma_str]:
                low_all_ma_flag = 0

            # and (max_index < ta_days * 9/10) and (max_index > ta_days*2/3) and (now_position <= 3)
    if (per_value < 25) and (max_index > ta_days*2/3) and low_all_ma_flag:
        return 1

    return 0


for root, dirs, files in os.walk(filedownloadpath):
    # root 表示当前正在访问的文件夹路径
    # dirs 表示该文件夹下的子目录名list
    # files 表示该文件夹下的文件list
    # 遍历文件
    for f in files:
        filepath = os.path.join(root, f)
        print(filepath)
        if method1(filepath) == 1:
            print(filepath[7:-5])
            for i in data.index.values:
                if data.loc[i, 'ts_code'] == filepath[7:-5]:
                    print(data.loc[i, 'ts_code'])
                    new_pd.append(data.loc[i])
        # os.remove(path)

good_date = datetime.datetime.now().date()
good_date_str = good_date.strftime('%Y%m%d')
dfnew = pd.DataFrame(new_pd)
writer = pd.ExcelWriter(resultpath + good_date_str + 'good.xlsx')
dfnew.to_excel(writer, sheet_name='good', index=False)
writer.save()

os.system('d:/催眠曲莫扎特.mp3')
