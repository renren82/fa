import pandas as pd

if __name__ == '__main__':
    df = pd.read_excel('D:/python/multiIndexTest.xlsx', sheet_name='合并利润表', header=[0, 1])

    print(df.head())
    print(df.loc[0, '本月发生'])
    print((df.loc[0, '本月发生'])['电力物流'])
    print((df.loc[0, '本月发生']).电力物流)