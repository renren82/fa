import pandas as pd
import os
from urllib import request
import matplotlib. pyplot as plt
import datetime
import time
import json
import faplt
import sendmails

path_root = "H:/"
# code_str = 'sz002403'
code_str = 'sz000559'
# code_str = 'sh000827'
# code_str_std = "002403.SZ"
# code_str_std = code_str[2:] + ".SZ"
freq = '5'
num = "1023"
# num = "256"
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
    l_power_list = []
    # df_data.fillna(np.nan）
    for k in df_data.index.values:
        if df_data.loc[k, 'trade_date'] == dt_base_delta_end_str:
            i=0
            # print（dt_base_delta_start_str)
            while df_data.loc[k+i, 'trade_date'] != dt_base_delta_start_str:
                # print(df_data.loc[k+i, 'ma5'])
                # if df_data.loc[k+i, 'ma5'].isna:
                #     return 0
                delta = df_data.loc[k+i, 'ma3'] - df_data.loc[k+i, 'ma5']
                delta = round(delta, 4)
                delta_value_list.append(delta)
                l_power_list.append(df_data.loc[k+i, 'power'])
                if type == 'up' or type == 'waveup':
                    l_price_list.append(df_data.loc[k+i, 'high'])
                else:
                    l_price_list.append(df_data.loc[k+i, 'low'])
                i+=1
            if type == 'up' or type == 'waveup':
                return float(max(delta_value_list)),  float(max(l_price_list)), float(max(l_power_list))
            else:
                return float(min(delta_value_list)), float(min(l_price_list)), float(min(l_power_list))
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
    df_data['ma5'] = ma5
    df_data['delta'] = df_data['ma3'] -df_data['ma5']
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


# if __name__ == '__main__':
def rt_process(code_str, freq):
    global mail_cnt
    #get  config
    df_param = pd.read_excel(path_root + path_param, dtype=str)
    # get data
    df = get_data(code_str, freq, num)
    # print(df.head())

    if file_exist(file_path):
        right_df = pd.read_excel(file_path, sheet_name='Sheet1', converters={'trade_date': str})
    else:
        right_df = pd.DataFrame(columns=['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol',
                               'amount', 'ma3', 'ma_v_3', 'ma5', 'ma_v_5'])

    if 'ma3' not in list(df):
        exit(0)
    df_new = pd.merge(df, right_df, how='outer')
    # if df_new.duplicated:
    #     df_new.drop_duplicates(keep='first').reset_index(drop=True)
    df_new.drop_duplicates(subset='trade_date', keep='first', inplace=True)
    df_new.reset_index(drop=True)

    # print(df_result.head())
    df_new['trade_date'] = pd.to_datetime(df_new['trade_date'], format="%Y%m%d%H%M%S")
    df_new.sort_values(by=['trade_date'], ascending=True, inplace=True, na_position='first')
    # print(df_result.head())
    vol3 = df_new.vol.rolling(window=3, center=False).mean()
    df_new['ma_v_3'] = vol3
    vol5 = df_new.vol.rolling(window=5, center=False).mean()
    df_new['ma_v_5'] = vol5
    ma3 = df_new.close.rolling(window=3, center=False).mean()
    df_new['ma3'] = ma3
    ma5 = df_new.close.rolling(window=5, center=False).mean()
    df_new['ma5'] = ma5
    df_new['delta'] = df_new['ma3'] - df_new['ma5']
    df_new['trade_date'] = df_new.trade_date.map(lambda X: X.strftime("%Y%m%d%H%M%S"))
    df_new = df_new.reindex(index=df_new.index[::-1])
    df_new = df_new.reset_index(drop=True)
    # print(df_new.head())
    # ---------------- -up is data ------------------------
    base_delta = -0.0180
    base_price = 8.01
    print(code_str + " " + 'base delta is ' + str(base_delta) + ' base price is ' + str(base_price))

    # -3%
    if df_new.loc[0, 'low'] <= 7.5:
        print(str(df_new.loc[0, 'low']) + " will cold ready to stop kui!")
        # os.system('E:/Tools/sound.wav')
        if mail_cnt < 5:
            mail_cnt += 1
            # sendmails.main()
    else:
        mail_cnt = 0

    # can't lower before segment
    if df_new.loc[0, 'delta'] <= -0.02467:
        print(str(df_new.loc[0, 'delta']) + " will cold ready to stop kui!")
        if mail_cnt < 5:
            mail_cnt += 1
            # sendmails.main()
            os.system('E:/Tools/sound.wav')
    else:
        mail_cnt = 0


    # hot_k = 40 # len(df_result.index.values)
    # bottom_k, fractal_count = back_enough_method(df_new, 0, hot_k)
    # if fractal_count >= 2:
    #     eval_down_delta(df_new, 0, 10)

    if datetime.datetime.now().hour > 15:
        writer_result = pd.ExcelWriter(file_out_path)
        df_new.to_excel(writer_result, index=False)
        writer_result.save()

    log_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
    print(log_time + " turn end")


# if __name__ == '__main__':
def ta_rt_main(code_str, freq, time_start):
    ta_rt_init(code_str, freq)
    while 1:
        rt_process(code_str, freq)
        # faplt.main(code_str + "_" + freq, '20201028093500')
        # faplt.main(code_str + "_" + freq, '20201230093500')
        # faplt.main(code_str + "_" + freq, '20210128145500')
        faplt.main(code_str + "_" + freq, time_start)
        # time.sleep(0.5)
        time.sleep(5)
        if datetime.datetime.now().hour > 15:
            break
