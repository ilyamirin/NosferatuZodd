

from re import match

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

table = read_excel('tariffs.xlsx')

cols = list(table.columns)
for i in range(len(cols)):
    if match('Unnamed:.*', cols[i]):
        cols[i] = prev_col
    prev_col = cols[i]

    # make banks dict with tariffs as values and
banks_tariff = {i: [] for i in cols[1:]}
for i, j in zip(cols[1:], table.loc[0][1:]):
    banks_tariff[i].append(j)

# cut off banks from table
table.columns = append(['хар-ка\тариф'], table.loc[0][1:])
table.loc[0] = cols
table = table.dropna(subset=['хар-ка\тариф'])
table = table.fillna('-')
for i in table:
    table[i] = table[i].astype(str)