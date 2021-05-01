
import tushare as ts
import os
import datetime
import numpy as np
# import talib
import pandas as pd
import gettdxdata
import resampledata
import resampledata_second
import powerdata
import fa
import faplt
import ta_rt

if __name__ == '__main__':
    if 0:
        gettdxdata.main()
        resampledata.main("sh000827_D", "M")
        powerdata.main('sh000827_M')
        powerdata.main('sh000827_D')
        fa.main()
        # faplt.main("000559.SZ_D", '20200115')
        # faplt.main("601633.SH_D", '20200629')
        # faplt.main("002403.SZ_D", '20190807')
        faplt.main("sh000827_D", '20191129')
        # faplt.main("300750.SZ_D", '20190611')
        # faplt.main("300059.SZ_D", "20200204")
        # faplt.main("000738.SZ_D", "20200401")
        # faplt.main("600893.SH_D", '20200615')
        # faplt.main("601012.SH_D", '20200820')
        faplt.main("603128.SH_D", '20181019')
        faplt.main("600429.SH_D", "20200204")

    if 0:
        # rt
        ta_rt.ta_rt_main('sz002403', '5', "20210302145500")

