import pandas as pd
# import matplotlib.pyplot as plt


path_root = 'H:/'
path_file = path_root + 'list.xlsx'

df = pd.read_excel(path_file, sheet_name='SSE')

print(df.head())
print(df['name'].head())
print(df.loc[1])
print(df.loc[1, 'name'])



