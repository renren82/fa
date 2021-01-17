import os
import datetime
import time
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path_root = 'H:/'
dt_now = datetime.datetime.now().date()
dt_now_str = dt_now.strftime('%Y%m%d')
dt_start = dt_now - datetime.timedelta(days=360*4)
dt_start_str = dt_start.strftime('%Y%m%d')


def get_area_data(industry):
    """
    get base delta value for ma3-ma5
    """
    # if os.path.exists(path_data):
    #     return 1
    industry_value = 0
    industry_cnt = 0
    df_list = pd.read_excel(path_root + "list.xlsx")

    for k in df_list.index.values:
        if df_list.loc[k, 'industry'] == industry:
            # asset	str	Y	资产类别：E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 CB可转债（v1.2.39），默认E
            # freq D W M
            df = ts.pro_bar(ts_code=df_list.loc[k, 'ts_code'], adj='qfq', start_date=dt_start_str,
                            end_date=dt_now_str, freq='D', ma=[3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 800])
            print(df.head())
            time.sleep(1)

            if df.loc[0, 'ma5'] > df.loc[0, 'close'] >= df.loc[0, 'ma3']:
                industry_value += 3
            if df.loc[0, 'ma8'] > df.loc[0, 'close'] >= df.loc[0, 'ma5']:
                industry_value += 5
            if df.loc[0, 'ma13'] > df.loc[0, 'close'] >= df.loc[0, 'ma8']:
                industry_value += 8
            if df.loc[0, 'ma21'] > df.loc[0, 'close'] >= df.loc[0, 'ma13']:
                industry_value += 13
            if df.loc[0, 'ma34'] > df.loc[0, 'close'] >= df.loc[0, 'ma21']:
                industry_value += 21
            if df.loc[0, 'ma55'] > df.loc[0, 'close'] >= df.loc[0, 'ma34']:
                industry_value += 34
            if df.loc[0, 'ma89'] > df.loc[0, 'close'] >= df.loc[0, 'ma55']:
                industry_value += 55
            if not np.isnan(df.loc[0, 'ma144']) and df.loc[0, 'ma144'] > df.loc[0, 'close'] >= df.loc[0, 'ma89']:
                industry_value += 89
            if not np.isnan(df.loc[0, 'ma233']) and not np.isnan(df.loc[0, 'ma144']) and df.loc[0, 'ma233'] > df.loc[0, 'close'] >= df.loc[0, 'ma144']:
                industry_value += 144
            if not np.isnan(df.loc[0, 'ma800']) and not np.isnan(df.loc[0, 'ma233']) and df.loc[0, 'ma800'] > df.loc[0, 'close'] >= df.loc[0, 'ma233']:
                industry_value += 233
            if not np.isnan(df.loc[0, 'ma800']) and df.loc[0, 'close'] >= df.loc[0, 'ma800']:
                industry_value += 800
            industry_cnt += 1

    print(industry_value/industry_cnt)


if __name__ == '__main__':
    get_area_data("汽车配件")