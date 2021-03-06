# -*- coding:utf-8 -*-
# @Auther: XiongGuoqing
# @Datetime: 2020/9/22 12:17 PM
# @Contact: xiong3219@icloud.com

from read_file import *
from genetic_algorithm import *
import copy
import sys

sys.setrecursionlimit(100000)

if __name__ == '__main__':
    # Initialize ALL Employees
    # 1 一工一人 -> 57.5
    employees_combination = ['P', 'D', 'F', 'B', 'T']
    # 2 一工多人
    # employees_combination = ['P', 'P', 'D', 'F', 'B', 'B', 'T']
    # 4 多面手
    # employees_combination = ['PD', 'D', 'F', 'BF', 'T']

    # Read data
    quest_address = './simplified_problem/'
    # quest_address = './complex_problem/'
    time_cost = read_dependence(quest_address + 'time_cost.csv', 'time')
    dependence_outer = read_dependence(quest_address + 'dependence_outer.csv',
                                       'outer')
    dependence_inner = read_dependence(quest_address + 'dependence_inner.csv',
                                       'inner')

    # Initialize Genetic Algorithm Model
    ppl_size = 500
    generation_max = 40
    mutation_rate = 0.6
    evolve_rate = 0.7
    walker_step = 0.015

    model_ga = GA(employees_combination=employees_combination,
                  ppl_size=ppl_size,
                  time_cost=time_cost,
                  dependence_inner=dependence_inner,
                  dependence_outer=dependence_outer,
                  walker_step=walker_step)

    print('\n')
    for generation in range(1, generation_max + 1):
        print('-' * 23, 'generation', generation, '-' * 23)
        population_original = copy.deepcopy(model_ga.population)

        select_list = model_ga.select(model_ga.population)
        children_origin = model_ga.crossover(select_list=select_list)

        fertility_rate = 100 * len(children_origin) / (
            len(population_original) / 2)
        print('生育率: {:.2f}%'.format(fertility_rate))

        mutation_rate = mutation_rate
        children_left = model_ga.mutate(children_origin=children_origin,
                                        mutation_rate=mutation_rate)

        if len(children_origin) != 0:
            print('变异存活率: {:.2f}%'.format(100 * len(children_left) /
                                          len(children_origin)))
        else:
            print('无子代，无法变异')

        if evolve_rate >= 0.4:
            evolve_rate -= 0.005
        population_left, best_fitness, best_group = model_ga.evolve(
            parents=population_original,
            children=children_left,
            evolve_rate=evolve_rate)

        population_diff = -(len(population_original) - len(population_left))
        print('种群数增减量: {}'.format(population_diff))
        print('当前种群总数: {}'.format(len(population_left)))
        print('当前最优适应度: {}'.format(best_fitness))

        if generation == generation_max:
            print('-' * 60)
            print('最优的种群为: ')
            for em in best_group.group_list:
                print(em.work_type, '\t:', em.DNA)

    # 输出求解过程
    # model_ga.get_fitness(best_group, test_flag=True)
