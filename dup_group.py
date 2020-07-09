import pandas as pd
data = pd.DataFrame({'产品': ['A', 'A', 'A', 'A'], '数量': [50, 50, 30, 30]})
if data.duplicated:
    dataA = data.drop_duplicates(keep='first').reset_index(drop=True)
print(dataA)
dataB = dataA.groupby(by='产品').agg({'数量': sum})
print('数据汇总结果:')
print(dataB)