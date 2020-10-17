import os
import datetime
import pandas as pd

path_root = 'H:/'
code_str = 'sz300059'
path_file = path_root + code_str + '_5min.xlsx'
path_result = path_root + code_str + '_60min.xlsx'


def gen_back_data(path_file_in, step, path_result_out):
    df = pd.read_excel(path_file_in, sheet_name='5min')
    df_new = pd.DataFrame(columns=['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol', 'amount', 'ma3',
                                   'ma_v_3', 'ma5', 'ma_v_5'])

    for i in range(0, max(df.index.values), step):
        df_new = df_new.append(df.loc[i + step - 1])
        df_new.loc[i + step - 1, 'open'] = df.loc[i, 'open']
        high_list = []
        for k in range(0, step - 1):
            high_list.append(df.loc[i + k, 'high'])
        df_new.loc[i + step - 1, 'high'] = max(high_list)
        low_list = []
        for k in range(0, step - 1):
            low_list.append(df.loc[i + k, 'low'])
        df_new.loc[i + step - 1, 'low'] = min(low_list)
        vol_list = []
        for k in range(0, step - 1):
            vol_list.append(df.loc[i + k, 'vol'])
        df_new.loc[i + step - 1, 'vol'] = sum(vol_list)

    vol3 = df_new.vol.rolling(window=3, center=False).mean()
    df_new['ma_v_3'] = vol3
    vol5 = df_new.vol.rolling(window=5, center=False).mean()
    df_new['ma_v_5'] = vol5

    ma3 = df_new.close.rolling(window=3, center=False).mean()
    df_new['ma3'] = ma3
    ma5 = df_new.close.rolling(window=5, center=False).mean()
    df_new['ma5'] = ma5

    df_new['delta'] = df_new['ma3'] - df_new['ma5']

    writer_delta = pd.ExcelWriter(path_result_out)
    df_new.to_excel(writer_delta, sheet_name='result', index=False)
    writer_delta.save()
    writer_delta.close()

    return


if __name__ == '__main__':
    gen_back_data(path_file, 12, path_result)

