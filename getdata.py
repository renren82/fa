import pandas as pd
import os
import requests
import matplotlib.pyplot as plt
import datetime

# codename = 'sz002403'
# codename = 'sh601989'
codename = 'sz000559'
title_name = 'wxqc'
freq = '30'
dt_now = datetime.datetime.now().date()
dt_now_str = dt_now.strftime('%Y%m%d')
path = 'H:/' + codename + '_' + freq + 'm_' + dt_now_str + '.xlsx'


def compute_power_data(df_data, k_start, k_end):
    """
     compute mean surface
    """
    i = k_end
    delta_sum = 0
    while i != k_start:
        delta_sum += df_data.loc[i, 'ma3'] - df_data.loc[i, 'ma5']
        df_data.loc[i, 'power'] = float(delta_sum / (k_end - i+1))
        # df_data.loc[i, 'power'] = float(delta_sum)
        i -= 1
    return 0


def compute_back_power_data(df_data, k_start, k_end):
    """
     compute mean surface
    """
    i = k_end
    delta_sum = 0
    while i <= k_start:
        delta_sum += df_data.loc[i, 'ma3'] - df_data.loc[i, 'ma5']
        df_data.loc[i, 'power'] = float(delta_sum / (i - k_end + 1))
        # df_data.loc[i, 'power'] = float(delta_sum)
        i += 1
    return 0


def power_back_data(df):
    '''
    power from ma3 - ma5
    surface
    '''
    k_start = len(df.index.values) - 1
    k_end = 0
    k = len(df.index.values) - 1
    while k > 0:
        if ((df.loc[k, 'ma3'] >= df.loc[k, 'ma5']) and (df.loc[k - 1, 'ma3'] < df.loc[k - 1, 'ma5'])) or (
                (df.loc[k, 'ma3'] <= df.loc[k, 'ma5']) and (df.loc[k - 1, 'ma3'] > df.loc[k - 1, 'ma5'])):
            k_end = k
            compute_back_power_data(df, k_start, k_end)
            k_start = k_end
        k -= 1


def power_data(df):
    k_start = -1
    k_end = 0
    k = 0
    for k in df.index.values:
        if ((df.loc[k, 'ma3'] >= df.loc[k, 'ma5']) and (df.loc[k + 1, 'ma3'] < df.loc[k + 1, 'ma5'])) or (
                (df.loc[k, 'ma3'] <= df.loc[k, 'ma5']) and (df.loc[k + 1, 'ma3'] > df.loc[k + 1, 'ma5'])):
            k_end = k
            compute_power_data(df, k_start, k_end)
            k_start = k_end



def get_sina_data(path, datanum):

    # if os.path.exists(path):
    #     return 1

    df = pd.DataFrame(columns=['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol',
                               'amount', 'ma3', 'ma_v_3', 'ma5', 'ma_v_5'])
    # df = pd.DataFrame({'ts_code' , 'trade_date' , 'open' , 'high' , 'low' , 'close' , 'vol' ,
    #                    'amount' , 'ma3' , 'ma_v_3' , 'ma5' , 'ma_v_5' })

    dataurl = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=' +\
              codename + '&scale=' + freq + '&ma=no&datalen=' + datanum

    content = requests.get(dataurl).text

    # data_list = content.split(',')
    # print(content)
    # print(data_list[3])

    # res = json.loads(content)
    # print(content)  # 打印字典
    # print(type(content))  # 打印res类型
    # print(content.keys())  # 打印字典的所有Key

    content = content.split('[')[1]

    content = content[1:len(content) - 2].split('},{')

    for i in range(0, len(content)):
        column = {}
        # print(content[i])
        dayData = content[i].split(',')
        for j in range(0, len(dayData)):
            field = dayData[j].split(':"')

            if field[0] == '\"day\"':
                column['trade_date'] = field[1].replace('"', '')
            elif field[0] == '\"volume\"':
                column['vol'] = field[1].replace('"', '')
            elif field[0] == '\"close\"':
                column['close'] = field[1].replace('"', '')
            elif field[0] == '\"open\"':
                column['open'] = field[1].replace('"', '')
            elif field[0] == '\"high\"':
                column['high'] = field[1].replace('"', '')
            elif field[0] == '\"low\"':
                column['low'] = field[1].replace('"', '')
            else:
                column[field[0]] = field[1].replace('"', '')

        # column['ma3'] = 0
        # column['ma5'] = 0
        # column['ma_v_3'] = 0
        # column['ma_v_5'] = 0
        column['ts_code'] = codename
        # print(column)
        df = df.append(column, ignore_index=True)

    # vol5 = df.vol.rolling(window=5, center=False).mean()
    # vol5 = vol5[start:end]
    vol3 = df.vol.rolling(window=3, center=False).mean()
    df['ma_v_3'] = vol3
    vol5 = df.vol.rolling(window=5, center=False).mean()
    df['ma_v_5'] = vol5

    ma3 = df.close.rolling(window=3, center=False).mean()
    df['ma3'] = ma3
    ma5 = df.close.rolling(window=5, center=False).mean()
    df['ma5'] = ma5

    df['delta'] = df['ma3'] - df['ma5']

    df['trade_date'] = pd.to_datetime(df['trade_date'], format="%Y-%m-%d %H:%M:%S")
    df['trade_date'] = df['trade_date'].dt.strftime('%Y%m%d%H%M%S')

    df = df.reindex(index=df.index[::-1])
    df = df.reset_index(drop=True)
    print(df.head())

    df.to_excel(path, sheet_name='Data', index=False)

    return 1


if __name__ == '__main__':

    get_sina_data(path, '256')

    '''
    plt 
    '''
    df = pd.read_excel(path)
    power_data(df)
    # df['trade_date'] = pd.to_datetime(df['trade_date'])
    # # x = df.loc[:, 'signal_date'].values
    # #
    # # y = df.loc[:, 'delta_%'].values
    #
    # df = df.set_index('trade_date')

    # df['close_%'] = df['close']

    plt.subplot(211)
    df['delta'].plot()
    # df['power'].plot(kind='bar', color='r')
    df['power'].plot()
#    plt.annotate('signal point', xy=(175, -0.05), xytext=(180, -0.1), arrowprops=dict(facecolor='red', shrink=0.05), )

    plt.gca().invert_xaxis()
    plt.legend()
    plt.grid(True)
    plt.ylabel('delta', size=15)
    plt.title(title_name)

    plt.subplot(212)
    df['close'].plot()
    plt.gca().invert_xaxis()
    plt.legend()
    plt.grid(True)
    plt.ylabel('close', size=15)
    # plt.title('title name')
    # plt.rcParams['savefig.dpi'] = 1024
    plt.show()