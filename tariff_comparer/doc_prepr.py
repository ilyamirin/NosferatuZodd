from re import match
from math import ceil
from numpy import append
from pandas import read_excel

def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return (arrs)

x = read_excel('20190901_Рынок пакеты.xlsx')

cols = list(x.columns)
for i in range(len(cols)):
    if match('Unnamed:.*', cols[i]):
        cols[i] = prev_col
    prev_col = cols[i]

    # make banks dict with tariffs as values and
banks_tariff = {i: [] for i in cols[1:]}
for i, j in zip(cols[1:], x.loc[0][1:]):
    banks_tariff[i].append(j)

# cut off banks from table
x.columns = append(['хар-ка\тариф'], x.loc[0][1:])
x = x[x['хар-ка\тариф'] != 'Тариф']
x = x.dropna(subset=['хар-ка\тариф'])
x = x.fillna('-')
for i in x:
    x[i] = x[i].astype(str)

print(x)