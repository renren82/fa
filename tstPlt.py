import pandas as pd
import matplotlib.pyplot as plt
# import numpy as np

path_root = 'H:/'
path_file = path_root + 'tst.xlsx'

df = pd.read_excel(path_file)

plt.scatter(df['x'], df['y'], marker='o', color='red', s=20, label='vol')

plt.grid(True)
# plt.ylabel('power', size=15)
# plt.gca().invert_xaxis()
plt.legend()

plt.show()