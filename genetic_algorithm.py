# -*- coding:utf-8 -*-
# @Auther: XiongGuoqing
# @Datetime: 2020/9/21 4:25 PM
# @Contact: xiong3219@icloud.com

import copy
import math
import logging
import itertools
import numpy as np
from work_object import Employee, Module, Group

logging.basicConfig(level=logging.NOTSET)


class cartesian(object):
    def __init__(self):
        self._data_list = []

    def add_list(self, data=[]):
        self._data_list.append(data)

    def build(self):
        return list(itertools.product(*self._data_list))


class GA(object):
    def __init__(self, employees_combination, ppl_size, time_cost,
                 dependence_inner, dependence_outer, walker_step):
        self.ppl_size = ppl_size
        self.timecost = time_cost
        self.dependence_outer = dependence_outer
        self.dependence_inner = dependence_inner
        self.walker_step = walker_step

        # Initialization Function Part
        logging.info('Initializing Module...')
        self.initialize_module()
        logging.info('Loading the Paths...')
        self.paths = self.load_path()
        logging.info('Initializing Population...')
        self.initialize_population(em_combination=employees_combination)

    def initialize_module(self):
        # Initialize ALL Module (Depend on the Dependence)
        self.outer_module = []
        self.inner_module = {}

        # Outer Dependence
        max_length = max(
            len(self.dependence_outer[i])
            for i in range(len(self.dependence_outer)))
        for round in range(1, max_length):
            for stack in self.dependence_outer:
                try:
                    if stack[round] not in self.outer_module:
                        module = Module(stack[round])
                        self.outer_module.append(module)
                    index = stack.index(stack[round])
                    id_former = stack[index - 1]
                    index_ = self.outer_module.index(stack[round])
                    self.outer_module[index_].add_dep(ID_former=id_former)
                except:
                    continue

        # Inner Dependence
        for key, val in self.dependence_inner.items():
            self.inner_module[key] = []
            for stack in val:
                for round in range(1, len(stack)):
                    if stack[round] not in self.inner_module[
                            key] and stack[round] != 0:
                        module = Module(stack[round])
                        self.inner_module[key].append(module)
                    id_former = stack[round - 1]
                    try:
                        index_ = self.inner_module[key].index(stack[round])
                        self.inner_module[key][index_].add_dep(
                            ID_former=id_former)
                        time = self.timecost[(key,
                                              self.inner_module[key][index_])]
                        self.inner_module[key][index_].add_time(time=time)
                        self.inner_module[key][index_].add_parent(key)

                    except:
                        continue
        # Sorting
        self.outer_module.sort()
        for key, val in self.inner_module.items():
            val.sort()

    def load_path(self):
        dependence_outer = copy.deepcopy(self.dependence_outer)
        dependence_inner = copy.deepcopy(self.dependence_inner)

        all_path = []
        all_path_out = []
        for path_out in dependence_outer:
            all_path_out.append(path_out[1:])
        for path_out in all_path_out:
            product = cartesian()
            for step in path_out:
                # pre-operate the array
                path_pre = copy.deepcopy(dependence_inner[step])
                path_list = []
                for path_p in range(len(path_pre)):
                    path_pre[path_p] = path_pre[path_p][1:]
                    while 0 in path_pre[path_p]:
                        path_pre[path_p].remove(0)
                    path = []
                    for p in range(len(path_pre[path_p])):
                        # path_pre[p] = str(step) + '.' + str(path_pre[p])
                        path.append(str(step) + '.' + str(path_pre[path_p][p]))
                    path_list.append(path)
                product.add_list(path_list)
            prodcut_out = product.build()
            for p_o in prodcut_out:
                path = []
                for p_o_ in p_o:
                    for p in p_o_:
                        path.append(p)
                all_path.append(path)
        return all_path

    def check_in(self, list1, list2):
        # check list1 in list2 or not
        res = [False for i in list1 if i not in list2]
        if res:
            return False
        else:
            return True

    # 检查DNA是否符合依赖关系的要求
    def check_rule(self, DNA, module):
        DNA_ = list(DNA)
        end_flag = len(DNA_)
        pop_stack = []
        for p in range(len(DNA_)):
            pop = DNA_.pop(0)
            if self.check_in(module[module.index(pop)].dependence, pop_stack):
                pop_stack.append(pop)
                if len(pop_stack) == end_flag:
                    return True
            else:
                return False

    def initialize_population(self, em_combination):
        # Another New Method to Initialize Population
        self.population = []

        def choose_available():
            available_list = []
            for path in paths:
                if len(path) != 0:
                    stack_top = path[0]
                else:
                    continue
                o, i = stack_top.split('.')
                # print(inner_module[int(o)])
                if outer_module[outer_module.index(
                        int(o)
                )].dependence == [] and inner_module[int(o)][inner_module[int(
                        o
                )].index(
                        int(i)
                )].dependence == [] and stack_top not in available_list:
                    available_list.append(stack_top)
            return available_list

        for p in range(self.ppl_size):
            print('\r', '生成中... 当前种群数:', p + 1, end='')
            self.initialize_module()
            outer_module = copy.deepcopy(self.outer_module)
            inner_module = copy.deepcopy(self.inner_module)
            paths = copy.deepcopy(self.paths)
            group = Group(group_id=int(p))
            for job in em_combination:
                em = Employee(work_type=job)
                em.DNA = []
                group.add_employee(em)
            while True:
                a_list = list(set(choose_available()))
                # choose from the a_list
                a_chosen = []
                while True:
                    chosen = np.random.choice(a_list, size=1)[0]
                    o, i = chosen.split('.')
                    # 如果是第一次选择
                    if a_chosen == []:
                        a_chosen.append(chosen)
                        # 给em加DNA
                        for em in group.group_list:
                            if em.work_type_num[0] == int(i):
                                em.DNA.append(int(o))
                        # 从alist中移除被选择的module
                        a_list.remove(a_list[a_list.index(chosen)])
                        # 从paths中移除
                        for path in paths:
                            try:
                                path.remove(chosen)
                            except:
                                continue
                        # 从inner_module中移除
                        inner_module[int(o)].remove(
                            inner_module[int(o)][inner_module[int(o)].index(
                                int(i))])
                        for inner in inner_module[int(o)]:
                            try:
                                inner.del_dep(int(i))
                            except:
                                continue
                        # 从outer_module中移除
                        if inner_module[int(o)] == []:
                            for outer in outer_module:
                                try:
                                    outer.del_dep(int(o))
                                except:
                                    continue
                    else:
                        flag = False
                        for c in a_chosen:
                            c_o, c_i = c.split('.')
                            if c_i == i:
                                # 多面手bug预留
                                flag = True
                        # 如果曾经选择的module中 没有与现在选择的module有工位冲突
                        # 那么就将这个选择的module添加进来 即flag==false
                        if flag is False:
                            a_chosen.append(chosen)
                            for em in group.group_list:
                                if em.work_type_num[0] == int(i):
                                    em.DNA.append(int(o))
                            a_list.remove(a_list[a_list.index(chosen)])
                            for path in paths:
                                try:
                                    path.remove(chosen)
                                except:
                                    continue
                            # 从inner_module中移除
                            inner_module[int(o)].remove(inner_module[int(o)][
                                inner_module[int(o)].index(int(i))])
                            for inner in inner_module[int(o)]:
                                try:
                                    inner.del_dep(int(i))
                                except:
                                    continue
                            # 从outer_module中移除
                            if inner_module[int(o)] == []:
                                for outer in outer_module:
                                    try:
                                        outer.del_dep(int(o))
                                    except:
                                        continue
                        # 若发生工位冲突 那么就再选一次
                        else:
                            continue
                    if a_list == []:
                        break
                    else:
                        c_i_list = []
                        a_i_list = []
                        for c in a_chosen:
                            c_o, c_i = c.split('.')
                            c_i_list.append(c_i)
                        for a in a_list:
                            a_o, a_i = a.split('.')
                            a_i_list.append(a_i)
                        if self.check_in(a_i_list, c_i_list):
                            break
                        else:
                            continue
                a_list_ = choose_available()
                # break条件
                if a_list_ == []:
                    group_sub = copy.deepcopy(group)
                    group.fitness, _ = self.get_fitness(group_sub)
                    self.population.append(group)
                    break

    def get_fitness(self, group):
        group_list = group.group_list
        fitness = 0

        self.initialize_module()

        outer_module = self.outer_module
        inner_module = self.inner_module
        paths = self.load_path()

        def choose_available():
            available_list = []
            for path in paths:
                if len(path) != 0:
                    stack_top = path[0]
                else:
                    continue
                o, i = stack_top.split('.')
                # print(inner_module[int(o)])
                if outer_module[outer_module.index(
                        int(o)
                )].dependence == [] and inner_module[int(o)][inner_module[int(
                        o
                )].index(
                        int(i)
                )].dependence == [] and stack_top not in available_list:
                    available_list.append(stack_top)
            return available_list

        while True:
            a_list = choose_available()
            mission_todo = []
            stack_top_list = []
            for em in group_list:
                try:
                    if int(em.DNA[0]) == 0:
                        em.DNA.pop(0)
                    stack_top = em.DNA[0]
                except:
                    stack_top = Module(-1)
                stack_top_list.append(stack_top)

                for a in a_list:
                    o, i = a.split('.')
                    if int(o) == int(stack_top) and int(i) == int(
                            em.work_type_num[0]):
                        mission_todo.append(a)

            time_min = None
            for mission in mission_todo:
                o, i = mission.split('.')
                i = inner_module[int(o)][inner_module[int(o)].index(int(i))]
                if time_min is None:
                    time_min = i.time
                elif i.time < time_min:
                    time_min = i.time
            try:
                fitness += float(time_min)
            except:
                fitness += 0

            for mission in mission_todo:
                o, i = mission.split('.')
                i = inner_module[int(o)][inner_module[int(o)].index(int(i))]
                try:
                    i.time -= time_min
                except:
                    pass
                if i.time == 0:
                    inner_module[int(o)].remove(int(i))
                    for path in paths:
                        if mission in path:
                            path.remove(mission)
                    for em in group_list:
                        try:
                            for dna in em.DNA:
                                if dna == int(
                                        o) and em.work_type_num[0] == int(i):
                                    em.DNA.pop(em.DNA.index(dna))
                        except:
                            continue
                    for mission_after in inner_module[int(o)]:
                        if int(i) in mission_after.dependence:
                            mission_after.del_dep(int(i))
                    if len(inner_module[int(o)]) == 0:
                        for out in outer_module:
                            if int(o) in out.dependence:
                                out.del_dep(int(o))
            if len(mission_todo) == 0:
                break

        succeed_key = True
        # 不光要判断外部依赖，还要判断内部依赖是否都消除干净，消除干净的才是能够求出fitness的
        # Oct 27 11:28 PM DONE!
        for ooo in outer_module:
            if len(ooo.dependence) != 0:
                succeed_key = False
        for iii in inner_module.values():
            if len(iii) != 0:
                succeed_key = False
        group.fitness = fitness
        return fitness, succeed_key

    def get_fitness_test(self, group):
        group_list = group.group_list
        fitness = 0

        self.initialize_module()

        outer_module = self.outer_module
        inner_module = self.inner_module

        def choose_available():
            available_list = []
            for i in outer_module:
                if i.status:
                    for j in inner_module[i]:
                        if j.status:
                            available_list.append(j)
            return available_list

        while True:
            print('-' * 30)
            a_list = choose_available()
            for a in a_list:
                print(a.parent, a, '|', end=' ')
            print('\n')
            mission_todo = []
            stack_top_list = []
            for em in group_list:
                try:
                    if int(em.DNA[0]) == 0:
                        em.DNA.pop(0)
                    stack_top = em.DNA[0]
                except:
                    stack_top = Module(-1)
                stack_top_list.append(stack_top)

                for a in a_list:
                    # 藏着问题：多面手 em.work_type_num[0]
                    if int(a.parent) == int(stack_top) and int(a.ID) == int(
                            em.work_type_num[0]):
                        # and a not in mission_todo
                        if a in mission_todo:
                            a_ = mission_todo[mission_todo.index(a)]
                            if a.parent != a_.parent:
                                mission_todo.append(a)
                        else:
                            mission_todo.append(a)

            for m_todo in mission_todo:
                print(m_todo.parent, m_todo, '|')

            time_min = None
            which_one_is_the_min = None
            for mission in mission_todo:
                if time_min is None:
                    time_min = mission.time
                    which_one_is_the_min = mission
                elif mission.time < time_min:
                    time_min = mission.time
                    which_one_is_the_min = mission
            try:
                print('(', time_min, ') |', which_one_is_the_min.parent,
                      which_one_is_the_min, '|')
            except:
                print('')
            try:
                fitness += float(time_min)
            except:
                fitness += 0
            for mission in mission_todo:
                try:
                    inner_module[mission.parent][inner_module[
                        mission.parent].index(mission)].time -= time_min
                except:
                    for em in group_list:
                        print(em.work_type_num, em.DNA)

                if inner_module[mission.parent][inner_module[
                        mission.parent].index(mission)].time == 0:
                    inner_module[mission.parent].remove(mission)
                    for em in group_list:
                        try:
                            for dna in em.DNA:
                                if dna == mission.parent and em.work_type_num[
                                        0] == mission:
                                    em.DNA.pop(em.DNA.index(dna))
                        except:
                            continue
                    for mission_after in inner_module[mission.parent]:
                        if mission in mission_after.dependence:
                            mission_after.del_dep(mission)
                    if len(inner_module[mission.parent]) == 0:
                        for out in outer_module:
                            if mission.parent in out.dependence:
                                out.del_dep(mission.parent)
            if len(mission_todo) == 0:
                break
        return fitness

    def calc_prob(self, fitness_list):
        transit_list = []
        prob_list = []
        for i in fitness_list:
            transit_list.append(1 - i / sum(fitness_list))
        for j in transit_list:
            prob_list.append(j / sum(transit_list))
        return prob_list

    def select(self, population):
        select_list = []
        fitness_list = []
        for group in population:
            fitness_list.append(group.fitness)
        prob_list = self.calc_prob(fitness_list=fitness_list)
        idx = np.random.choice(population,
                               size=len(population),
                               replace=False,
                               p=prob_list)
        for i in range(0, len(idx), 2):
            try:
                select_list.append([idx[i], idx[i + 1]])
            except:
                continue
        return select_list

    def crossover(self, select_list):
        child_num = self.ppl_size
        children = []
        for parents in select_list:
            father = parents[0]
            mother = parents[1]
            # 为了不让child的id和父母的重复（保证内存空间不一样）
            child = Group(group_id=child_num)
            # 杂交规则：随机从父母获得一半的员工DNA
            f_prob, m_prob = 0.5, 0.5
            walker = float(self.walker_step)
            for f_em, m_em in zip(father.group_list, mother.group_list):
                child_em = np.random.choice([f_em, m_em],
                                            size=1,
                                            p=[f_prob, m_prob])[0]
                if child_em == f_em:
                    f_prob -= walker
                    m_prob += walker
                elif child_em == m_em:
                    f_prob += walker
                    m_prob -= walker
                child.add_employee(child_em)
            child_out = copy.deepcopy(child)
            fitness, key = self.get_fitness(child)
            if key:
                children.append(child_out)
                child_num += 1
        return children

    def nucleotide_exchange(self, DNA):
        m, n = np.random.choice(DNA, size=2, replace=False)
        mark1, mark2 = DNA.index(m), DNA.index(n)
        DNA[mark1], DNA[mark2] = n, m
        return DNA

    def mutate(self, children_origin, mutation_rate):
        child_left = []
        for child in children_origin:
            # Every child is a Group
            for em in child.group_list:
                random = np.random.rand()
                if random < mutation_rate:
                    em.DNA = self.nucleotide_exchange(em.DNA)
            child_out = copy.deepcopy(child)
            fitness, key = self.get_fitness(child)
            if key:
                child_out.fitness = fitness
                child_left.append(child_out)
        return child_left

    def get_threshold(self, fitness_list, evolve_rate):
        fitness_list.sort()
        maximum = max(fitness_list)
        minimun = min(fitness_list)
        threshold = (maximum - minimun) * evolve_rate
        threshold += minimun

        return threshold, minimun

    # 筛选部分的Group将其淘汰 包含父母合并
    def evolve(self, parents, children, evolve_rate):
        def ppl_sort(ppl):
            ppl_sorted = []
            for group in ppl:
                fitness = group.fitness
                if ppl_sorted != []:
                    for group_ in ppl_sorted:
                        fitness_ = group_.fitness
                        flag = False
                        if fitness <= fitness_:
                            ppl_sorted.insert(
                                ppl_sorted.index(group_) + 1, group)
                            flag = True
                            break
                    if flag is False:
                        ppl_sorted.append(group)
                else:
                    ppl_sorted.append(group)
            return ppl_sorted

        population_merge = []
        fitness_list = []
        for p in parents:
            population_merge.append(p)
            fitness_list.append(p.fitness)
        for c in children:
            population_merge.append(c)
            fitness_list.append(c.fitness)

        threshold, minimum = self.get_threshold(fitness_list=fitness_list,
                                                evolve_rate=evolve_rate)
        best_group = None
        for g in population_merge:
            if g.fitness == minimum:
                best_group = g
                break
        population_left = []
        # ppl_merge = population_merge.sort(key=self.get_fitness, reverse=True)
        ppl_merge = ppl_sort(population_merge)
        for pop in ppl_merge:
            if pop.fitness <= threshold and len(population_left) < 500:
                population_left.append(pop)
            else:
                continue
        if len(population_left) <= 1:
            print('***触发防灭绝保护***')
            population_left.append(population_merge[0])
            population_left.append(population_merge[1])
        self.population = population_left
        self.initialize_module
        return population_left, minimum, best_group
