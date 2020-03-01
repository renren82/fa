import pandas as pd
import os

df = pd.read_excel('48周现场故障数据.xlsx', sheet_name='1-4000')

dfExtr = pd.DataFrame()

new_pd = []
for i in df.index.values:
    if df.loc[i, '所属部门'] == '显示器':
        new_pd.append(df.loc[i])
    #    print(i)

dfnew = pd.DataFrame(new_pd)
dfExtr = dfExtr.append(dfnew, ignore_index=True)

print(dfExtr)

filepath = os.path.dirname(os.path.abspath(__file__)) + "/简报提取.xlsx"
dfExtr.to_excel(filepath, index=False)


print('简报提取')