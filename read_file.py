# -*- coding:utf-8 -*-
# @Auther: XiongGuoqing
# @Datetime: 2020/9/22 7:18 PM
# @Contact: xiong3219@icloud.com

import csv

def read_dependence(file, data_type):
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        if data_type == 'outer':
            dependence_outer = []
            for row in reader:
                for i in range(len(row)):
                    row[i] = int(row[i])
                row.insert(0, -1)
                dependence_outer.append(row)
            return dependence_outer
        elif data_type == 'inner':
            dependence_inner = {}
            for row in reader:
                for i in range(len(row)):
                    row[i] = int(row[i])
                row.insert(1, -1)
                if row[0] not in dependence_inner.keys():
                    dependence_inner[row[0]] = [list(row[1:])]
                else:
                    dependence_inner[row[0]].append(row[1:])
            return dependence_inner
        elif data_type == 'time':
            time_cost = {}
            for row in reader:
                for i in range(len(row)):
                    if i != len(row) - 1:
                        row[i] = int(row[i])
                    else:
                        row[i] = float(row[i])
                time_cost[(row[0], row[1])] = row[-1]
            return time_cost


