from tabulate import tabulate
import random as r
headers = ['Question', 'Visited Count', 'Last Visited']
data = []

'''
for testing tables

'''
for i in range(10):
    res = []
    res.append(str(r.randint(2000, 10000)))
    res.append(str(r.randint(1, 40)))
    res.append(f'{r.randint(2,10)} days ago.')
    data.append(res)

print(tabulate(data, headers=headers, tablefmt='fancy_grid',
               numalign='center', stralign='center'))
