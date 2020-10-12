# -*- coding:utf-8 -*-
# @Auther: XiongGuoqing
# @Datetime: 2020/9/23 4:46 PM
# @Contact: xiong3219@icloud.com

for em in group:
    # print(em, em.work_type, em.DNA)
    '''
    ['P'] [1] [2, 6, 4, 7, 8, 5, 3]
    ['D'] [2] [6, 0, 4, 7, 8, 5, 3]
    ['F'] [3] [6, 2, 4, 7, 8, 3, 5]
    ['B'] [4] [6, 2, 7, 4, 3, 8, 5]
    ['T'] [5] [6, 2, 7, 8, 5, 4, 3]
    '''
    a_list = choose_available()
    # num = 1
    # print(a_list, a_list[num].parent, a_list[num].ID)
    '''
    [1, 1, 2] 6 1
    [1, 1, 2] 6 1
    [1, 1, 2] 6 1
    [1, 1, 2] 6 1
    [1, 1, 2] 6 1
    '''
    # 这里有个bug，没有考虑到多面手的问题
    for nuc in em.DNA:
        nuc_ex = Module(em.work_type[0])
        if int(nuc) != 0:
            nuc_ex.add_parent(int(nuc))
        for a in a_list:
            if nuc_ex.ID == a.ID and nuc_ex.parent == a.parent:
                a_list.remove(a)