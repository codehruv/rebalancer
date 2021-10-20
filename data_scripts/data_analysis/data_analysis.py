import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("eth_dex_data.csv")

with open('output.txt', 'w') as f:
    for col in list(data.columns.values):
        print(col, file=f)

f.close()