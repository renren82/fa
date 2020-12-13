
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

if __name__ == '__main__':
    # gettdxdata.main()
    # resampledata.main()
    # powerdata.main('sh000827_M')
    # powerdata.main('sh000827_D')
    fa.main()
    faplt.main("002403.SZ_D", '20190807')
    # faplt.main("sh000827_D", '20191129')
    # faplt.main("300059.SZ_D", "20200204")