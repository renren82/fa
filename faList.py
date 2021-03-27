
import tushare as ts
import os
import datetime
import numpy as np
# import talib
import pandas as pd

# set parameter
ta_days = 144
filedownloadpath = 'H:/'


dt_end = datetime.datetime.now().date()
dt_start = dt_end - datetime.timedelta(days=ta_days)

dt_end_str = dt_end.strftime('%Y%m%d')
dt_start_str = dt_start.strftime('%Y%m%d')


# ts.set_token('2e2ec7b610512cc2704e3aa692711794ad9cacf7a2cae31ee0a769bf')

pro = ts.pro_api( )

# 输入参数
#
# 名称	类型	必选	描述
# is_hs	str	N	是否沪深港通标的，N否 H沪股通 S深股通
# list_status	str	N	上市状态： L上市 D退市 P暂停上市
# exchange	str	N	交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
# 输出参数
#
# 名称	类型	描述
# ts_code	str	TS代码
# symbol	str	股票代码
# name	str	股票名称
# area	str	所在地域
# industry	str	所属行业
# fullname	str	股票全称
# enname	str	英文全称
# market	str	市场类型 （主板/中小板/创业板）
# exchange	str	交易所代码
# curr_type	str	交易货币
# list_status	str	上市状态： L上市 D退市 P暂停上市
# list_date	str	上市日期
# delist_date	str	退市日期
# is_hs	str	是否沪深港通标的，N否 H沪股通 S深股通
data = pro.stock_basic(exchange='SSE', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# print(type(data))
writer = pd.ExcelWriter(filedownloadpath + 'list.xlsx')
data.to_excel(writer, sheet_name='SSE', index=False)
writer.save()

for i in data.index.values:
    print(data.loc[i, 'ts_code'])
    ts_code_str = data.loc[i, 'ts_code']
    path = filedownloadpath + ts_code_str + '.xlsx'
    df = ts.pro_bar(ts_code=ts_code_str, adj='qfq', start_date=dt_start_str, end_date=dt_end_str, ma=[3, 5, 55])
    writer = pd.ExcelWriter(path)
    # print(type(df).__name__)
    if type(df).__name__ == 'DataFrame':
        df.to_excel(writer, sheet_name='history', index=False)
        writer.save()


# df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
# df = ts.get_realtime_quotes(['600460','000762','000725'])

# print(df.head())

# file_path = os.path.dirname(os.path.abspath(__file__)) + "/000001SZ.xlsx"
# df.to_excel(file_path)


# data = pro.stock_basic(exchange='SZSE', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# print(data.head())


# df=ts.get_k_data('600600')
# df['MA10_rolling'] = pd.rolling_mean(df['close'],10)
# close = [float(x) for x in df['close']]
# # 调用talib计算10日移动平均线的值
# df['MA10_talib'] = talib.MA(np.array(close), timeperiod=10)
# df.tail(12)