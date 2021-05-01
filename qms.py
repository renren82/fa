import pandas as pd


def indexOfstr(s1, s2):
    if type(s1) == float:
        return -1

    if s2 in s1:
        return 1
    else:
        return -1

    # n1 = len(s1)
    # n2 = len(s2)
    #
    # for i in range(n1-n2+1):
    #     if s1[i:i+n2] == s2:
    #         return 1
    #     else:
    #         return -1


#
df = pd.read_excel('350.xlsx', sheet_name='sheet1', converters={'问题类别/模式': str})
# df = pd.read_excel('yy.xlsx',  converters={'故障描述':str})

dfx = pd.read_excel('信息.xlsx', sheet_name='sheet1', converters={'问题描述': str})

dfMy = pd.read_excel('05.xlsx', sheet_name='中标动')

# print(df.head())
# print(dfMy.head())
# if '17车报网络中央控制单元' in '2019年07月04日配属北京局北京南动车所CR400AF-B-2121列动车组库内检修时17车报网络中央控制单元1 MVB通信故障，复位后故障消除':
#      print('find ok')
# else:
#     print('not find')

# s = '17车报网络中央控制单元'
# s = '01车报ETB通信故障' not find
# s = '13车报编组网交换机1ECN通讯故障'

# 分析进度
s_list = ['不报卫生间故障', '无轴温数据', '全列报编组网交换机1ECN通信故障', '2062列', 'WTB通信故障']
index = 0

for s in s_list:
    flag = 0
    for i in df.index.values:
        # print(df.loc[i, '问题描述'])
        if indexOfstr(df.loc[i, '问题类别/模式'], s) == 1:
            # print('find ok: ', index)
            for j in dfMy.index.values:
                if indexOfstr(dfMy.loc[j, '故障描述'], s) == 1:
                    dfMy.loc[j, '分析进展'] = df.loc[i, '进展情况（直接在原有基础上更新）']
                    dfMy.loc[j, '后续计划'] = df.loc[i, '后续工作计划']
                    # dfMy.loc[j, '分析进展'] = df.loc[i, '分析进展']
                    # dfMy.loc[j, '后续计划'] = df.loc[i, '后续计划']
                    flag = 1
                    break

    if flag == 0:
        for i in dfx.index.values:
            if indexOfstr(dfx.loc[i, '问题描述'], s) == 1:
                # print('find ok: ', index)
                for j in dfMy.index.values:
                    if indexOfstr(dfMy.loc[j, '故障描述'], s) == 1:
                        dfMy.loc[j, '分析进展'] = dfx.loc[i, '进展']
                        # dfMy.loc[j, '后续计划'] = dfx.loc[i, '下一步计划']
                        flag = 1
                        break

    if flag == 1:
        print('find ok: ', index)
    else:
        print('not find: ', index, ' ', s)
    index += 1

writer = pd.ExcelWriter('my简报.xlsx')
dfMy.to_excel(writer, sheet_name='中标动')
writer.save()

print('helloworld-key')

