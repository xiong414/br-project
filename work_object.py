# -*- coding:utf-8 -*-
# @Auther: XiongGuoqing
# @Datetime: 2020/9/22 2:03 PM
# @Contact: xiong3219@icloud.com

import numpy as np


# Inherit the list, and add work_series

class Employee(object):
    def __init__(self, work_type):
        self.work_type = work_type
        self.work_type_num = []
        self.DNA = []
        type_switch = {'P': 1, 'D': 2, 'F': 3, 'B': 4, 'T': 5}
        for i in work_type:
            self.work_type_num.append(type_switch.get(i))


class Module(int):
    def __init__(self, ID):
        int.__init__(ID)
        self.ID = ID
        self.dependence = []
        self.time = 0
        self.refresh_status()
        self.parent = None

    def refresh_status(self):
        if len(self.dependence) == 0:
            self.status = True
        else:
            self.status = False

    def add_dep(self, ID_former):
        if ID_former != -1 and ID_former not in self.dependence:
            self.dependence.append(ID_former)
            self.refresh_status()

    def del_dep(self, dependence_id):
        self.dependence.remove(dependence_id)
        self.refresh_status()

    def add_time(self, time):
        self.time = time

    def add_parent(self, parent):
        self.parent = parent


class Group(object):
    def __init__(self, group_id):
        self.group_id = group_id
        self.group_list = []
        self.fitness = None

    def add_employee(self, em):
        self.group_list.append(em)
