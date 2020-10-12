# -*- coding:utf-8 -*-
# @Auther: XiongGuoqing
# @Datetime: 2020/9/21 4:25 PM
# @Contact: xiong3219@icloud.com

import copy
import math
import logging
import numpy as np
from work_object import Employee, Module, Group

logging.basicConfig(level=logging.NOTSET)


class GA_ppl(object):
    def __init__(self,
                 ppl_size,
                 evolve_rate,
                 mutation_rate,
                 walker_step,
                 dependence,
                 output_size):
        self.ppl_size = ppl_size
        self.evolve_rate = evolve_rate
        self.mutation_rate = mutation_rate
        self.walker_step = walker_step
        self.dependence = dependence
        self.output_size = output_size
        self.match_DNA = []
        self.init_rule()
        self.init_ppl()

    def init_rule(self):
        self.rule = []
        max_length = max(len(self.dependence[i])
                         for i in range(len(self.dependence)))
        for round in range(1, max_length):
            for stack in self.dependence:
                try:
                    if stack[round] not in self.rule:
                        module = Module(stack[round])
                        self.rule.append(module)
                    index = stack.index(stack[round])
                    id_former = stack[index - 1]
                    index_ = self.rule.index(stack[round])
                    self.rule[index_].add_dep(ID_former=id_former)
                except:
                    continue
        self.DNA_length = len(self.rule)

    def init_ppl(self):
        self.DNA_set = []
        # 初始化原始种群
        for p in range(self.ppl_size):
            DNA = list(self.rule)
            np.random.shuffle(DNA)
            self.DNA_set.append(DNA)

    def get_fitness(self, DNA):
        def check_in(list1, list2):
            res = [False for i in list1 if i not in list2]
            if res:
                return False
            else:
                return True

        fitness = 0
        rule = copy.deepcopy(self.rule)
        DNA = list(copy.deepcopy(DNA))
        pop_stack = []
        for p in range(len(DNA)):
            pop = DNA.pop(0)
            if check_in(rule[rule.index(pop)].dependence, pop_stack):
                pop_stack.append(pop)
                fitness += 1
        return fitness

    def select(self, DNA_set):
        # 两种类型的概率分布
        def softmax(fitness_list):
            softmax_list = []
            exp_sum = 0
            # print(fitness_list)
            for i in fitness_list:
                exp_sum += math.exp(i)
            for j in fitness_list:
                softmax_list.append(math.exp(j) / exp_sum)
            return softmax_list

        def calc_prob(fitness_list):
            prob_list = []
            for i in fitness_list:
                prob_list.append(i / sum(fitness_list))
            return prob_list

        DNA_set = copy.deepcopy(DNA_set)
        select_list = []
        fitness_list = []
        for DNA in DNA_set:
            fitness_list.append(self.get_fitness(DNA))
        prob_list = softmax(fitness_list=fitness_list)
        # prob_list = calc_prob(fitness_list=fitness_list)
        DNA_set_idx = [i for i in range(len(DNA_set))]
        idx = np.random.choice(DNA_set_idx, size=len(
            DNA_set), replace=False, p=prob_list)
        for i in range(0, len(idx), 2):
            try:
                select_list.append([DNA_set[idx[i]], DNA_set[idx[i + 1]]])
            except:
                continue
        return select_list

    def crossover(self, select_list):
        children = []
        for parents in select_list:
            father = copy.deepcopy(parents[0])
            mother = copy.deepcopy(parents[1])
            end_flag = len(father)
            child = []
            f_prob, m_prob = 0.5, 0.5
            walker = float(self.walker_step)

            while True:
                f = father[0]
                m = mother[0]
                c = np.random.choice([f, m], size=1, p=[f_prob, m_prob])[0]
                if c == f:
                    f_prob -= walker
                    m_prob += walker
                elif c == m:
                    f_prob += walker
                    m_prob -= walker
                child.append(c)
                father.remove(c)
                mother.remove(c)
                if len(child) == end_flag:
                    break
            children.append(child)
        print('孩子数: {}'.format(len(children)))
        return children

    def mutate(self, children):
        def nucleotide_exchange(DNA):
            m, n = np.random.choice(DNA, size=2, replace=False)
            mark1, mark2 = DNA.index(m), DNA.index(n)
            DNA[mark1], DNA[mark2] = n, m
            return DNA

        for child, idx in zip(children, range(len(children))):
            r = np.random.rand()
            if r < self.mutation_rate:
                child_new = nucleotide_exchange(child)
                children[idx] = child_new
        return children

    def evolve(self, parents, children):
        def get_threshold(fitness_list, evolve_rate):
            fitness_list.sort()
            maximum = max(fitness_list)
            minimum = min(fitness_list)
            threhold = (maximum - minimum) * (1 - evolve_rate)
            threhold += minimum

            return threhold, maximum

        ppl_merge = []
        fitness_list = []
        for p in parents:
            ppl_merge.append(p)
            fitness_list.append(self.get_fitness(p))
        for c in children:
            ppl_merge.append(c)
            fitness_list.append(self.get_fitness(c))

        threshold, maximum = get_threshold(fitness_list, self.evolve_rate)

        ppl_left = []
        for ppl in ppl_merge:
            if self.get_fitness(ppl) >= threshold and len(ppl_left) < 2000:
                ppl_left.append(ppl)
                if self.get_fitness(ppl) == self.DNA_length:
                    self.match_DNA.append(ppl)
        self.DNA_set = ppl_left
        return ppl_left, maximum

    def get_DNA(self, address):
        # output_DNA = []
        # if len(self.match_DNA) >= self.output_size:
        #     for o in range(self.output_size):
        #         output_DNA.append(self.match_DNA[o])
        #     return output_DNA
        # else:
        #     print('DNA生成量不足 {}/{}'.format(len(self.match_DNA), self.output_size))
        #     return self.match_DNA
        with open(address, 'w', encoding='utf8') as f:
            f.writelines(str(self.DNA_length) + ',' + str(len(self.match_DNA)))
            for dna in self.match_DNA:
                f.writelines(dna)


class GA(object):
    def __init__(self,
                 employees_combination,
                 ppl_size,
                 time_cost,
                 dependence_inner,
                 dependence_outer,
                 walker_step):
        self.ppl_size = ppl_size
        self.timecost = time_cost
        self.dependence_outer = dependence_outer
        self.dependence_inner = dependence_inner
        self.walker_step = walker_step

        # Initialization Function Part
        logging.info('Initializing Module...')
        self.initialize_module()
        logging.info('Initializing Population...')
        self.initialize_population(em_combination=employees_combination)

    def initialize_module(self):
        # Initialize ALL Module (Depend on the Dependence)
        self.outer_module = []
        self.inner_module = {}

        # Outer Dependence
        max_length = max(len(self.dependence_outer[i]) for i in range(
            len(self.dependence_outer)))
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
                    if stack[round] not in self.inner_module[key] and stack[round] != 0:
                        module = Module(stack[round])
                        self.inner_module[key].append(module)
                    id_former = stack[round - 1]
                    try:
                        index_ = self.inner_module[key].index(stack[round])
                        self.inner_module[key][index_].add_dep(
                            ID_former=id_former)
                        time = self.timecost[(
                            key, self.inner_module[key][index_])]
                        self.inner_module[key][index_].add_time(time=time)
                        self.inner_module[key][index_].add_parent(key)

                    except:
                        continue
        # Sorting
        self.outer_module.sort()
        for key, val in self.inner_module.items():
            val.sort()

    def check_in(self, list1, list2):
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
        # Initialize the Population and DNA
        self.population = []
        for p in range(self.ppl_size):
            while True:
                self.initialize_module()
                outer_module = self.outer_module
                group = Group(group_id=str(p))
                group_buffer = Group(group_id=int(p))
                for job in em_combination:
                    em = Employee(work_type=job)
                    em_buffer = Employee(work_type=job)
                    while True:
                        DNA = list(outer_module)
                        np.random.shuffle(DNA)
                        if self.check_rule(DNA=DNA, module=outer_module):
                            em.DNA = DNA
                            DNA_ = copy.deepcopy(DNA)
                            em_buffer.DNA = DNA_
                            # 防止某个员工的工作顺序表中含有不存在的工作，例如2.2
                            for d in DNA:
                                if em.work_type_num[0] not in self.inner_module[d]:
                                    DNA[DNA.index(d)] = Module(0)
                                    DNA_[DNA_.index(d)] = Module(0)
                            break
                    group.add_employee(em)
                    # print('got a employee!!!')
                    print(em.DNA)
                    group_buffer.add_employee(em_buffer)

                fitness, key = self.get_fitness(group=group)

                group_buffer.fitness = copy.deepcopy(group.fitness)
                if key:
                    self.population.append(group_buffer)
                    print(p + 1, '/', self.ppl_size)
                    # print('Append 1 group!', fitness, key)
                    break
                else:
                    continue

    def get_fitness(self, group):
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
                    # 藏着问题：多面手 em.work_type_num[0]
                    if int(a.parent) == int(stack_top) and int(a.ID) == int(em.work_type_num[0]):
                        # and a not in mission_todo
                        if a in mission_todo:
                            a_ = mission_todo[mission_todo.index(a)]
                            if a.parent != a_.parent:
                                mission_todo.append(a)
                        else:
                            mission_todo.append(a)

            time_min = None
            for mission in mission_todo:
                if time_min is None:
                    time_min = mission.time
                elif mission.time < time_min:
                    time_min = mission.time
            try:
                fitness += float(time_min)
            except:
                fitness += 0
            for mission in mission_todo:
                try:
                    inner_module[mission.parent][inner_module[mission.parent].index(
                        mission)].time -= time_min
                except:
                    pass

                if inner_module[mission.parent][inner_module[mission.parent].index(mission)].time == 0:
                    inner_module[mission.parent].remove(mission)
                    for em in group_list:
                        try:
                            for dna in em.DNA:
                                if dna == mission.parent and em.work_type_num[0] == mission:
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
                    if int(a.parent) == int(stack_top) and int(a.ID) == int(em.work_type_num[0]):
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
                    inner_module[mission.parent][inner_module[mission.parent].index(
                        mission)].time -= time_min
                except:
                    for em in group_list:
                        print(em.work_type_num, em.DNA)

                if inner_module[mission.parent][inner_module[mission.parent].index(mission)].time == 0:
                    inner_module[mission.parent].remove(mission)
                    for em in group_list:
                        try:
                            for dna in em.DNA:
                                if dna == mission.parent and em.work_type_num[0] == mission:
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
                child_em = np.random.choice(
                    [f_em, m_em], size=1, p=[f_prob, m_prob])[0]
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
            # for em in g.group_list:
            #     print(em.DNA)
            # print('.'*30)
            if g.fitness == minimum:
                best_group = g
                break
        population_left = []
        for pop in population_merge:
            if pop.fitness < threshold:
                population_left.append(pop)
        self.population = population_left
        self.initialize_module
        return population_left, minimum, best_group
