import pandas as pd
import os
from urllib import request
import matplotlib. pyplot as plt
import datetime
import time
import json
import faplt
import sendmails
import talib as ta
import math

path_root = "H:/"
# code_str = 'sz002403'
code_str = 'sz000559'
# code_str = 'sh000827'
# code_str_std = "002403.SZ"
# code_str_std = code_str[2:] + ".SZ"
freq = '30'
# num = "1023"
num = "256"
file_path = path_root + code_str + "_" + freq + '.xlsx'
# file_out_path = path_root + code_str_std + "_" + freq + '_new.xlsx'
file_out_path = path_root + code_str + "_" + freq + '.xlsx'

mail_cnt = 0

path_param = 'fa.xlsx'
dt_now = datetime.datetime.now().date()
dt_now_str = dt_now.strftime('%Y%m%d')
row_dic = {'high_price_date': "",'sellL_signal_date': '', 'delta':
0.0, 'delta_base': 0.0,'delta_%': 0.0, 'high': 0.0, 'high_base':
0.0,'high_%': 0.0 }
df_result = pd.DataFrame()
action_dir = {'k': 0, 'action': ""}
action_list = []





def ta_rt_init(code_str, freq ):
    global file_path, file_out_path
    file_path = path_root + code_str + "_" + freq + '.xlsx'
    # file_out_path = path_root + code_str_std + "_" + freq + '_new.xlsx'
    file_out_path = path_root + code_str + "_" + freq + '.xlsx'


def delta_base_3ma_5ma(df_data, type, dt_base_delta_start_str, dt_base_delta_end_str):
    """
    get base delta and base high
    """
    # sheet_name='Sheet1'
    # df_data = pd.read_excel(filepath, converters=
    # 'trade_date':str)
    # #
    # if 'ma3' not in list(df_data):
    # return 0
    #dtbase_ delta_start=
    # datetime. datetime. strptime(dt_base_delta_start_str,
    # %Y%m%d").date()
    # #dt base delta_end
    #  datetime. datetime. strptime(dt_base_ delta_end_str,
    #  %Y%m%d").date(
    # #n_days=dt_base_delta_end
    #  dt_base_delta_start).days
    l_price_list = []
    delta_value_list = []
    # l_power_list = []
    # df_data.fillna(np.nan）
    for k in df_data.index.values:
        if df_data.loc[k, 'trade_date'] == dt_base_delta_start_str :
            i=0
            # print（dt_base_delta_start_str)
            while df_data.loc[k+i, 'trade_date'] != dt_base_delta_end_str:
                # print(df_data.loc[k+i, 'ma5'])
                # if df_data.loc[k+i, 'ma5'].isna:
                #     return 0
                delta = df_data.loc[k+i, 'ma3'] - df_data.loc[k+i, 'ma5']
                delta = round(delta, 4)
                delta_value_list.append(delta)
                # l_power_list.append(df_data.loc[k+i, 'power'])
                if type == 'up' or type == 'waveup':
                    l_price_list.append(df_data.loc[k+i, 'high'])
                else:
                    l_price_list.append(df_data.loc[k+i, 'low'])
                i+=1
            if type == 'up' or type == 'waveup':
                return float(max(delta_value_list)),  float(max(l_price_list)) # , float(max(l_power_list)）
            else:
                return float(min(delta_value_list)), float(min(l_price_list))  #, float(min(l_power_list))
    return 0, 0, 0

def back_enough_method(df, start_k, end_k):
    i = start_k
    bottom_k =0
    fractal_count = 0
    min_low_p = 10000
    while i < end_k-2:
        m = i
        while df.loc[m, 'low'] == df.loc[m+1, 'low']:
            m += 1
        if df. loc[m, 'low'] > df. loc[m+1, 'low']:
            n = m+1
            while df. loc[n, 'low'] == df. loc[n+1, 'low']:
                n += 1
            if df.loc[n, 'low'] < df.loc[n+1, 'low']:
                if min_low_p >  df.loc[n, 'low']:
                    min_low_p = df.loc[n,'low']
                    fractal_count = 0
                    bottom_k = m + 1
                else:
                    if bottom_k != 0:
                        fractal_count += 1
        print('bottom_k: '+ str(bottom_k) + " fractal_count:" + str(fractal_count))
        i+=1
    return bottom_k, fractal_count

def eval_down_delta(df, start_k, end_k):
    min_low_p =  df['low'].min()
    min_delta = df['delta'].min()
    cur_min_low_p =  df.loc[start_k:end_k, 'low'].min()
    cur_min_delta = df.loc[start_k:end_k, 'delta']. min()
    if cur_min_low_p > min_low_p and 0 > cur_min_delta > min_delta:
        print('down power is not bigger')
        action_dir['k'] = end_k
        action_dir['action'] = 'b'
        action_list. append(action_dir)
    print('cur_min_low_p:' + str(cur_min_low_p) + "cur_min_delta:"+str(cur_min_delta))


def get_data(codename, freq, datanum):
    df_data = pd.DataFrame(columns=['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol'
    'amount', 'ma3', 'ma_v_3', 'ma5', 'ma_v_51'])
    # url_30m = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine30m?symbol='
    # url = url_30m + "M0"

    url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=' +\
              codename + '&scale=' + freq + '&ma=no&datalen=' + datanum

    req = request.Request(url)

    rsp = request.urlopen(req)
    res = rsp.read()
    res_json = json.loads(res)
    # res=json.loads(content)
    # print(content)#打印字典
    # print(type(content))#打印res类型
    # print(content.keys()#打印字典的所有Key
    # res_json.reverse()
    # print(res_json)
    for line in res_json:
        # print(line)
        column = {}
        date_format = datetime.datetime.strptime(line['day'], '%Y-%m-%d %H:%M:%S')  # 格式化日期
        column['trade_date'] = date_format.strftime("%Y%m%d%H%M%S")
        column['open'] = float(line['open'])
        column['high'] = float(line['high'])
        column['low'] = float(line['low'])
        column['close'] = float(line['close'])
        column['vol'] = int(line['volume'])
        column['ts_code'] = codename
        df_data = df_data.append(column, ignore_index=True)
    #vol5  = df.vol.rolling(window=5, center=False).mean()
    #vol5 =  vol5[start:end]
    ma3 = df_data.close.rolling(window=3, center=False).mean()
    df_data['ma3'] = ma3
    ma5 = df_data.close.rolling(window=5, center=False).mean()
    ma13 = df_data.close.rolling(window=13, center=False).mean()
    df_data['ma5'] = ma5
    df_data['delta'] = df_data['ma3'] -df_data['ma5']
    df_data['ma13'] = ma13
    # df_data.to_excel(path, index=False)
    return df_data


def eval_hot_cold(i, df_param, df_data, base_delta_value, base_price, base_power):
    hot_cold_k = 0
    dt_tst = datetime.datetime.strptime(df_param.loc[i, 'cur_start'], '%Y%m%d').date()
    delta_max = 0
    delta_max_rate = 0
    delta_max_date = ""
    delta_rate_max = 0
    high_low_price = 0
    power_max = 0
    high_low_price_date = ""
    if df_param.loc[i, 'type'] == 'up':
        df_param.loc[i,'status'] = 'not hot'
    else:
        df_param.loc[i,'status'] = 'not cold'
    while dt_tst <= dt_now:
        dt_tst_str = dt_tst.strftime('%Y%m%d')
        global df_result
        for k in df_data. index. values:
            # print(type(df_data.loc[k, 'trade_date'l))
            if df_data.loc[k, 'trade_date'] == dt_tst_str:
                delta_pre = float(df_data.loc[k+1, 'ma3'] - df_data.loc[k+1, 'ma5'])
                delta_now = float(df_data.loc[k, 'ma3'] - df_data.loc[k, 'ma5'])
        if df_param.loc[i,'type'] == 'up' or df_param.loc[i, 'type'] == 'waveup':
            if delta_max <= delta_now:
                delta_max = delta_now
                delta_max_date = dt_tst_str
                delta_rate = round((delta_now - base_delta_value)*100/base_delta_value, 4)
                if power_max <= df_data.loc[k, 'power']:
                    power_max = df_data.loc[k, 'power']
                if delta_now >= base_delta_value:
                    print(df_param.loc[i, 'name'] +" " + dt_tst_str + 'is hot: ' + str(delta_rate)+' % delta')
                    df_param.loc[i, 'status'] = 'hot'
                if delta_pre >= base_delta_value and delta_now < delta_pre:
                    signal_price_list[df_data.loc[k, 'high']]
                    j = 1
                    while float(df_data.loc[j, 'ma3'] - df_data.loc[k+j, 'ma5']) >= base_delta_value:
                        # signal_price_list.append (df_data.loc[k+i, high'])
                        if high_low_price <= df_data.loc[k+j, 'high']:
                            high_low_price = df_data.loc[k+j, 'high']
                            high_low_price_date = df_data.loc[k+j, 'trade_date']
                        j += 1
                    print(df_param.loc[i, 'name'] + '' + dt_tst_str + 'is hot and beichi, high price' + str(high_low_price))
                    df_param.loc[i, 'status'] = 'hot and beichi'
                    action_dir['K'] = k
                    action_dir['action'] = 's'
                    action_list.append(action_dir)
                    hot_cold_k = k
                    # high=max(signal_price_list)
                    if high_low_price >= base_price:
                        row_dic['sell_signal_date'] = dt_tst_str
                        row_dic['delta'] = delta_pre
                        row_dic['delta_base'] = base_delta_value
                        row_dic['delta_%'] = (delta_pre - base_delta_value)*100 / base_delta_value
                        row_dic['high'] = high_low_price
                        row_dic['high_base'] = base_price
                        row_dic['high%'] = (high_low_price - base_price)*100 / base_price
                        df_result = df_result.append(row_dic, ignore_index=True)
        if df_param.loc[i, 'type'] == 'down' or  df_param.loc[i, 'type'] == 'wavedown':
            if delta_max >= delta_now:
                delta_max = delta_now
                delta_maxdate = dt_tst_str
                delta_rate = round((delta_now - base_delta_value) * 100 / (base_delta_value), 4)
                # print(str(delta_rate)
            if delta_now <= base_delta_value:
                print(df_param.loc[i, 'name']+ "" + dt_tst_str + 'is cold: '+str(delta_rate)+ '% delta')
                df_param.loc[i, 'status'] = 'cold'
        dt_tst = dt_tst + datetime.timedelta(days=1)
    # print(delta_rate_max_date + 'is max hot: '+ str(delta_rate_max) + '% delta')
    df_param.loc[i, 'cur_max_delta_date'] = delta_max_date
    df_param.loc[i, 'cur_max_delta'] = delta_max
    df_param.loc[i, 'curmax_delta_rate'] = str(delta_rate) + "%"
    df_param.loc[i, 'cur_max_power']= power_max
    # df_param.loc[i, 'cur_high_low_price'] = high_low_price
    # df_param.loc[i, 'cur_high_low_price_date'] =  high_low_price_date
    print('end')
    return hot_cold_k


def file_exist(path):
    # return 0
    if os.path.exists(path):
        return 1
    else:
        return 0


class dingding_man:
    def __init__(self, code_str, freq, num, ma_price, base_price, n):
        self.mail = 0
        self.code_str = code_str
        self.freq = freq
        self.num = num
        self.ma_price = ma_price
        self.base_price = base_price
        self.zhouqi = n

        self.compare_delta = 0
        self.pre_delta = 0
        self.pre_ma3 = 0
        self.pre_ma5 = 0
        self.pre3_close = 0
        self.pre5_close = 0

    def up(self):
        df = get_data(self.code_str, self.freq, self.num)
        id = df.index.values.max()
        menkan = self.ma_price + (df.loc[id, 'close'] - self.base_price) / self.zhouqi
        # print(menkan)
        if df.loc[id, 'close'] >= (menkan-0.02):
            # log_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
            snd_str = self.code_str + " " + str(df.loc[id, 'close']) + " up available"
            print(snd_str)
            if self.mail < 1:
                self.mail += 1
                sendmails.main(snd_str)
        else:
            self.mail = 0

    def down(self):
            df = get_data(self.code_str, self.freq, self.num)
            id = df.index.values.max()
            menkan = self.ma_price + (df.loc[id, 'close'] - self.base_price)/ self.zhouqi
            print(menkan)
            if df.loc[id, 'close'] <= (menkan):
                # log_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
                snd_str = self.code_str + " " + str(df.loc[id, 'close']) + " down available"
                print(snd_str)
                if self.mail < 1:
                    self.mail += 1
                    sendmails.main(snd_str)
            else:
                self.mail = 0

    def boll_lower(self):
        df = get_data(self.code_str, self.freq, self.num)
        # print(df.close[-20:])
        uper, middle, lower = ta.BBANDS(df.close[-20:].values,  timeperiod=20,
                # number of non-biased standard deviations from the mean
                nbdevup=2,
                nbdevdn=2,
                # Moving average type: simple moving average here
                matype=0)
        # print(str(uper[-1]) + " " + str(middle[-1]) + " " + str(lower[-1]))

        if df.close.values[-1] <= (lower[-1]):
            # log_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
            snd_str = self.code_str + " " + str(df.close.values[-1]) + " boll lower available"
            print(snd_str)
            if self.mail < 1:
                self.mail += 1
                sendmails.main(snd_str)
        else:
            self.mail = 0

    def baolifang_afterjuewangdown(self, base_start, base_end):
        df = get_data(self.code_str, self.freq, self.num)
        previousdelta, lowprice = delta_base_3ma_5ma(df, "down", base_start, base_end)
        # print(previousdelta)
        # print(lowprice)
        base = ((-previousdelta)*0.9)
        print(base)
        for k in df.index.values:
            if df.loc[k, 'trade_date'] == base_end:
                for i in range(k, len(df.index.values)):
                    if (df.loc[i, 'ma3']-df.loc[i, 'ma5']) >= base:
                        snd_str = self.code_str + " " + str(df.loc[i, 'trade_date']) + " " + str(df.loc[i, 'close']) + " hot available"
                        print(snd_str)
                        if self.mail < 1:
                            self.mail += 1
                            sendmails.main(snd_str)
                    else:
                        self.mail = 0

    def zhudiup_init(self, name, level):
        df_param = pd.read_excel("h:/fa.xlsx", dtype=str)
        for k in df_param.index.values:
            # print(df_param.loc[k, 'code'])
            # print(type(df_param.loc[k, 'code']))
            if type(df_param.loc[k, 'code']) == float and math.isnan(df_param.loc[k, 'code']) is True:
                # print("continue")
                continue
            if df_param.loc[k, 'code'] == name and df_param.loc[k, 'level'] == level:
                self.compare_delta = float(df_param.loc[k, 'compare_delta'])
        print(self.compare_delta)
        df_data = pd.read_excel("h:/"+name+"_D.xlsx", converters={'trade_date': str})
        if 'ma3' not in list(df_data):
            return 0
        self.pre_delta = df_data.loc[0, "delta"]
        self.pre_ma3 = df_data.loc[0, "ma3"]
        self.pre_ma5 = df_data.loc[0, "ma5"]
        self.pre3_close = df_data.loc[2, "close"]
        self.pre5_close = df_data.loc[4, "close"]

    def zhudiup_beichi(self):
        if datetime.datetime.now().hour > 14 and datetime.datetime.now().minute >= 0:
            df = get_data(self.code_str, self.freq, self.num)
            id = df.index.values.max()
            ma3 = self.pre_ma3 + (df.loc[id, 'close'] - self.pre3_close) / 3
            ma5 = self.pre_ma5 + (df.loc[id, 'close'] - self.pre5_close) / 5
            delta = ma3 - ma5
            print(delta)
            if self.pre_delta >= self.compare_delta and delta < self.pre_delta:
                # log_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
                snd_str = self.code_str + " " + str(df.loc[id, 'close']) + " " + str(delta) + " beichi available"
                print(snd_str)
                if self.mail < 1:
                    self.mail += 1
                    sendmails.main(snd_str)
            elif delta >= self.compare_delta:
                snd_str = self.code_str + " " + str(df.loc[id, 'close']) + " " + str(delta) + " hot available"
                print(snd_str)
                if self.mail < 1:
                    self.mail += 1
                    sendmails.main(snd_str)
            else:
                self.mail = 0


if __name__ == '__main__':
    up1 = dingding_man(code_str, freq, num, 8.22, 4.08, 89) # 89M
    down1 = dingding_man("sz002797", "60", "21", 7.39, 6.86, 13)
    down2 = dingding_man("sz000559", "60", "21", 0, 0, 0)
    d1cy = dingding_man("sz002797", "30", "256", 0, 0, 0)
    asd = dingding_man("sz002403", "30", "5", 0, 0, 0)
    asd.zhudiup_init("002403.SZ", "筑底段")
    dycy = dingding_man("sz002797", "30", "5", 0, 0, 0)
    dycy.zhudiup_init("002797.SZ", "筑底段2")
    zgzg = dingding_man("sh601989", "30", "5", 0, 0, 0)
    zgzg.zhudiup_init("601989.SH", "筑底段2")
    while 1:
        try:
            # up1.up()
            # down1.boll_lower()
            # down2.boll_lower()
            d1cy.baolifang_afterjuewangdown("20210903140000", "20210917140000")
            asd.zhudiup_beichi()
            dycy.zhudiup_beichi()
            zgzg.zhudiup_beichi()

        except Exception as r:
            print('未知错误 %s' % r)
            pass

        time.sleep(2)
        if datetime.datetime.now().hour > 15:
            break