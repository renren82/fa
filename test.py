import tushare as ts

"""
数据频度 ：支持分钟(min)/日(D)/周(W)/月(M)K线，其中1min表示1分钟（类推1/5/15/30/60分钟） ，默认D
"""
# df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011', freq='1min', ma=[3, 5])
# print(df.head())

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
