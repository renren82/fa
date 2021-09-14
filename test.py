import tushare as ts
import pandas as pd
import os
import datetime


"""
数据频度 ：支持分钟(min)/日(D)/周(W)/月(M)K线，其中1min表示1分钟（类推1/5/15/30/60分钟） ，默认D
"""
# df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011', freq='1min', ma=[3, 5])
# # print(df.head())

# Single stock symbol
df = ts.get_realtime_quotes('000581')
df[['code', 'name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']]


"""
0：name，股票名字
1：open，今日开盘价
2：pre_close，昨日收盘价
3：price，当前价格
4：high，今日最高价
5：low，今日最低价
6：bid，竞买价，即“买一”报价
7：ask，竞卖价，即“卖一”报价
8：volume，成交量 maybe you need do volume/100
9：amount，成交金额（元 CNY）
10：b1_v，委买一（笔数 bid volume）
11：b1_p，委买一（价格 bid price）
12：b2_v，“买二”
13：b2_p，“买二”
14：b3_v，“买三”
15：b3_p，“买三”
16：b4_v，“买四”
17：b4_p，“买四”
18：b5_v，“买五”
19：b5_p，“买五”
20：a1_v，委卖一（笔数 ask volume）
21：a1_p，委卖一（价格 ask price）
...
30：date，日期；
31：time，时间；

"""
print(df)


pro = ts.pro_api()

# 查询当前所有正常上市交易的股票列表
# is_hs	str	N	是否沪深港通标的，N否 H沪股通 S深股通
# list_status	str	N	上市状态： L上市 D退市 P暂停上市，默认L
# exchange	str	N	交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
# 名称	类型	描述
# ts_code	str	TS代码
# symbol	str	股票代码
# name	str	股票名称
# area	str	所在地域
# industry	str	所属行业
# fullname	str	股票全称
# enname	str	英文全称
# market	str	市场类型 （主板/中小板/创业板/科创板）
# exchange	str	交易所代码
# curr_type	str	交易货币
# list_status	str	上市状态： L上市 D退市 P暂停上市
# list_date	str	上市日期
# delist_date	str	退市日期
# is_hs	str	是否沪深港通标的，N否 H沪股通 S深股通

data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date, market, is_hs')

writer_delta = pd.ExcelWriter('H:/list.xlsx')
data.to_excel(writer_delta, sheet_name='Sheet1', index=False)
writer_delta.save()
writer_delta.close()


dt_1 = datetime.datetime.strptime('20190611', '%Y%m%d').date()
# 20190504
# 20190426
dt_2 = datetime.datetime.strptime('20190504', '%Y%m%d').date()

print((dt_1 - dt_2).days)

df = pd.read_excel("qms_new.xlsx", sheet_name='Sheet1')
print(df["装车车型"].mode())
print(df["装车车号"].mode())

x_list = []
for i in range(0, 100):
    x_list.append(i)
x_list.append(40)
x_list.append(50)
x_list.append(40)

print(df["value"].mean()) # pingjunzhi
df = pd.DataFrame(x_list, columns=["value"])
print(df["value"].mode()) # zhongshu
print(df["value"].std()) # biaozhuncha
print(df["value"].var()) # fangcha
print(df["value"].median()) # zhongweishu
print(df["value"].min()) # min
print(df["value"].max()) # max
print(df["value"].sum()) # sum