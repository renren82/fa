
import tushare as ts
import os
import datetime
import numpy as np
# import talib
import pandas as pd
import gettdxdata
import resampledata
import powerdata
import fa
import faplt
import ta_rt

if __name__ == '__main__':
    if 1:
        # gettdxdata.main()
        # resampledata.main("sh000827_D", "M")
        # powerdata.main('sh000827_M')
        # powerdata.main('sh000827_D')
        fa.main()
        faplt.main("002797.SZ_D", '20210510')
        faplt.main("000559.SZ_D", '20200115')
        # faplt.main("000559.SZ_15min", '202106211445')
        # faplt.main("601633.SH_D", '20200629')
        faplt.main("002403.SZ_D", '20181019')
        faplt.main("sh000827_D", '20191129')
        faplt.main("300750.SZ_D", '20190611')
        # faplt.main("300059.SZ_D", "20200204")
        # faplt.main("000738.SZ_D", "20200401")

        # faplt.main("600893.SH_D", '20200615')
        faplt.main("601012.SH_D", '20200820')
        # faplt.main("603128.SH_D", '20181019')
        # faplt.main("600429.SH_D", "20200204")

    if 0:
        df = ts.pro_bar(ts_code='000559.SZ', adj='qfq', start_date='202106211445', end_date='202107091500', freq='15min', ma=[3, 5])
        print(df.head())


