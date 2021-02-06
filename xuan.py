import os
import datetime
import time
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sendmails

path_root = 'H:/'
dt_now = datetime.datetime.now().date()
dt_now_str = dt_now.strftime('%Y%m%d')
dt_start = dt_now - datetime.timedelta(days=360*4)
dt_start_str = dt_start.strftime('%Y%m%d')
save_gupiao_data = 1

def get_area_data(df_list, industry):
    """
    get base delta value for ma3-ma5
    """
    # if os.path.exists(path_data):
    #     return 1
    industry_cnt = 0
    x_list = []
    for k in df_list.index.values:
        if df_list.loc[k, 'industry'] == industry:
            v_list = []
            # asset	str	Y	资产类别：E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 CB可转债（v1.2.39），默认E
            # freq D W M
            df = ts.pro_bar(ts_code=df_list.loc[k, 'ts_code'], adj='qfq', start_date=dt_start_str,
                            end_date=dt_now_str, freq='D', ma=[3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 800])
            print(df.head())
            time.sleep(1)
            if 'ma3' not in list(df):
                continue
            industry_value = 0
            # if df.loc[0, 'ma5'] > df.loc[0, 'close'] >= df.loc[0, 'ma3']:
            #     industry_value = 3
            if df.loc[0, 'close'] >= df.loc[0, 'ma3']:
                industry_value = 3
            if df.loc[0, 'close'] >= df.loc[0, 'ma5']:
                industry_value = 5
            if df.loc[0, 'close'] >= df.loc[0, 'ma8']:
                industry_value = 8
            if df.loc[0, 'close'] >= df.loc[0, 'ma13']:
                industry_value = 13
            if df.loc[0, 'close'] >= df.loc[0, 'ma21']:
                industry_value = 21
            if df.loc[0, 'close'] >= df.loc[0, 'ma34']:
                industry_value = 34
            if df.loc[0, 'close'] >= df.loc[0, 'ma55']:
                industry_value = 55
            if not np.isnan(df.loc[0, 'ma89']) and df.loc[0, 'close'] >= df.loc[0, 'ma89']:
                industry_value = 89
            if not np.isnan(df.loc[0, 'ma144']) and df.loc[0, 'close'] >= df.loc[0, 'ma144']:
                industry_value = 144
            if not np.isnan(df.loc[0, 'ma233']) and df.loc[0, 'close'] >= df.loc[0, 'ma233']:
                industry_value = 233
            if not np.isnan(df.loc[0, 'ma800']) and df.loc[0, 'close'] >= df.loc[0, 'ma800']:
                industry_value = 800

            v_list.append(df_list.loc[k, 'ts_code'])
            v_list.append(df_list.loc[k, 'name'])
            v_list.append(industry_value)
            x_list.append(v_list)

    df_op = pd.DataFrame(x_list, columns=["ts_code", "name", "value"])
    # print(df["value"].mode())  # zhongshu
    # print(df["value"].std())  # biaozhuncha
    # print(df["value"].var())  # fangcha
    # print(df["value"].median())  # zhongweishu
    # print(df["value"].min())  # min
    # print(df["value"].max())  # max
    # print(df["value"].sum())  # sum

    if save_gupiao_data == 1:
        writer_delta = pd.ExcelWriter(path_root + industry + ".xlsx")
        df_op.to_excel(writer_delta, sheet_name='Sheet1', index=False)
        writer_delta.save()
        writer_delta.close()

    return df_op["value"].mode()[0],  df_op["value"].mean(), df_op["value"].median(),  df_op["value"].min(), df_op["value"].max(), df_op["value"].std(), df_op["value"].var()


if __name__ == '__main__':
    df_xuan = pd.DataFrame(columns=['industry', 'mode', "mean", "median", "min", "max", "std", "var"])
    df_list = pd.read_excel(path_root + "list.xlsx", converters={'symbol': str})

    table = pd.pivot_table(df_list, index=["industry"])
    # print(table.head())
    # writer_delta = pd.ExcelWriter("H:/tst.xlsx")
    # table.to_excel(writer_delta, sheet_name='Sheet1', index=True)
    # writer_delta.save()
    # writer_delta.close()

    column = {}
    # for k in table.index.values:
    #     column['mode'], column["mean"], column["median"], column["min"], column["max"], column["std"], column["var"] = get_area_data(df_list, k)
    #     column['industry'] = k
    #     print(column)
    #     df_xuan = df_xuan.append(column, ignore_index=True)
    #
    # writer_delta = pd.ExcelWriter(path_root + "xuan.xlsx")
    # df_xuan.to_excel(writer_delta, sheet_name='Sheet1', index=False)
    # writer_delta.save()
    # writer_delta.close()
    # sendmails.main()

    k = "家用电器"
    column['mode'], column["mean"], column["median"], column["min"], column["max"], column["std"], column["var"] = get_area_data(df_list, k)
    print(column)

