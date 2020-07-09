import pandas as pd
import os

file_path_all = '0-标动250-成品基线--技术状态确认-all.xlsx'
# file_path_all = '0-标动250-信息化--基线--技术状态确认-all.xlsx'
path_result = '0-标动250-成品基线--技术状态确认-result.xlsx'
file_dir = 'P:/project/python/QA/change_files/'

file_all_df = pd.read_excel(file_path_all, sheetname='基线-汇总')
file_all_df = file_all_df.reset_index()
# print(file_all_df.head())

list_file = os.listdir(file_dir)
for file_name in list_file:
    file_path = file_dir + file_name
    print(file_path)
    file_df = pd.read_excel(file_path, sheetname='基线-汇总')
    file_df = file_df.reset_index()

    for i in file_all_df.index.values:
        # print(type(file_all_df.loc[i, '编号']))
        # print(i)
        # print(file_all_df.loc[i, '编号'])
        for j in file_df.index.values:
            # print(type(file_df.loc[j, '开发性质']))
            if file_all_df.loc[i, '编号'] != 'nan' and file_all_df.loc[i, '编号'] == file_df.loc[j, '编号']:
                # print('ok')
                if type(file_df.loc[j, '开发性质']) == str and file_df.loc[j, '开发性质'] != 'nan':
                    file_all_df.loc[i] = file_df.loc[j]
                    print(file_df.loc[j, '开发性质'])


writer_delta = pd.ExcelWriter(path_result)
file_all_df.to_excel(writer_delta, sheet_name='基线-汇总', index=False)
writer_delta.save()