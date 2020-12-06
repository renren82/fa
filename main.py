
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
    # fa.main()
    faplt.main("000559.SZ_D", '20200630')