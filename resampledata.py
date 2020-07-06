import os
import datetime
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

ts_code_str = 'sh000827_d'
resample_step = 'M'
path_root = 'H:/'
path_file = path_root + ts_code_str + '.xlsx'
file_result = path_root + ts_code_str + '_' + resample_step +".xlsx"


def resample_tdxdata(step):
        cycle_df = pd.DataFrame()
        df = pd.read_excel(path_file, sheet_name='day')
        df.trade_date = pd.to_datetime(df.trade_date, format="%Y%m%d")
        df.set_index('trade_date', inplace=True)

        cycle_df['close'] = df['close'].resample(rule=step).last()  # last：取这5分钟的最后一行数据
        # 开、高、低的价格，成交量
        cycle_df['open'] = df['open'].resample(rule=step).first()  # 五分钟内的第一个值就是开盘价
        cycle_df['high'] = df['high'].resample(rule=step).max()  # 五分钟内的最高价就是High
        cycle_df['low'] = df['low'].resample(rule=step).min()  # 五分钟内的最低价就是low
        cycle_df['vol'] = df['vol'].resample(rule=step).sum()

        vol3 = cycle_df.vol.rolling(window=3, center=False).mean()
        cycle_df['ma_v_3'] = vol3
        vol5 = cycle_df.vol.rolling(window=5, center=False).mean()
        cycle_df['ma_v_5'] = vol5

        ma3 = cycle_df.close.rolling(window=3, center=False).mean()
        cycle_df['ma3'] = ma3
        ma5 = cycle_df.close.rolling(window=5, center=False).mean()
        cycle_df['ma5'] = ma5

        cycle_df['delta'] = cycle_df['ma3'] - cycle_df['ma5']

        writer_delta = pd.ExcelWriter(file_result)
        cycle_df.to_excel(writer_delta, sheet_name=step, index=True)
        writer_delta.save()
        writer_delta.close()


if __name__ == '__main__':
    resample_tdxdata(resample_step)