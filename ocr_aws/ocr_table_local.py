import pandas as pd
import csv
import numpy as np

lista = ['AI_000-1.csv', 'AI_001-1.csv', 'AI_002-1.csv', 'AI_003-1.csv', 'AI_004-1.csv', 'AI_005-1.csv', 'AI_006-1.csv',
         'AI_007-1.csv']
for i in lista:
    with open(f'../csv/{i}') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = []
        for a in [row for row in csv_reader if row]:
            line_count.append([element.lower().strip() for element in a])

        for list_index in line_count:
            for item in list_index:
                if 'amount' in item:
                    item = ''
                else:
                    pass
        print('######################################################')
