# -*- coding:utf-8 -*-
# @Auther: XiongGuoqing
# @Datetime: 2020/9/22 12:17 PM
# @Contact: xiong3219@icloud.com

from read_file import *
from genetic_algorithm import *
import copy

if __name__ == '__main__':
    # Initialize ALL Employees
    employees_combination = ['P', 'D', 'F', 'B', 'T']

    # Read data
    # quest_address = './simplified_problem/'
    quest_address = './complex_problem/'
    time_cost = read_dependence(quest_address + 'time_cost.csv', 'time')
    dependence_outer = read_dependence(quest_address + 'dependence_outer.csv',
                                       'outer')
    dependence_inner = read_dependence(quest_address + 'dependence_inner.csv',
                                       'inner')

    # Initialize Genetic Algorithm Model
    ppl_size = 100
    generation_max = 50
    mutation_rate = 0.3
    evolve_rate = 0.7
    walker_step = 0.01

    model_ga = GA(employees_combination=employees_combination,
                  ppl_size=ppl_size,
                  time_cost=time_cost,
                  dependence_inner=dependence_inner,
                  dependence_outer=dependence_outer,
                  walker_step=walker_step)

    # all_path = model_ga.load_path()
    # for path in all_path:
    #     stack_top = path[0]
    #     o, i = stack_top.split('.')
    #     print(type(o), type(i), model_ga.outer_module[model_ga.outer_module.index(int(o))].dependence)

    print('\n')
    for generation in range(1, generation_max + 1):
        print('-' * 20, 'generation', generation, '-' * 20)
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

        evolve_rate -= 0.002
        # model_ga.evolve(parents=population_original, children=children_left, evolve_rate=evolve_rate)
        population_left, best_fitness, best_group = model_ga.evolve(
            parents=population_original,
            children=children_left,
            evolve_rate=evolve_rate)

        population_diff = -(len(population_original) - len(population_left))
        print('种群数增减量: {}'.format(population_diff))
        print('当前种群总数: {}'.format(len(population_left)))
        print('当前最优适应度: {}'.format(best_fitness))

        if generation == generation_max:
            print('-' * 55)
            print('最优的种群为: ')
            for em in best_group.group_list:
                print(em.work_type_num[0], em.DNA)

    # print('-' * 55)
    # print('最优种群的求解过程: ')
    # print(model_ga.get_fitness_test(group=best_group))

    # # --------------- DNA INITIALZATION ---------------

    # ga_ppl = GA_ppl(ppl_size=100,
    #                 evolve_rate=0.75,
    #                 mutation_rate=0.4,
    #                 walker_step=0.01,
    #                 dependence=dependence_outer,
    #                 output_size=10)

    # gen = 0
    # while True:
    #     print('-' * 20, 'generation', gen, '-' * 20)
    #     select_ppl_list = ga_ppl.select(ga_ppl.DNA_set)
    #     children = ga_ppl.crossover(select_ppl_list)

    #     children_left = ga_ppl.mutate(children)

    #     ppl_left, ppl_dead, maximum, max_count, minimum, threshold = ga_ppl.evolve(
    #         parents=ga_ppl.DNA_set, children=children_left)

    #     if ga_ppl.evolve_rate >= 0.1 and max_count >= 5 and float(maximum - threshold) >= 1.0:
    #         ga_ppl.evolve_rate -= 0.01
    #     elif ga_ppl.evolve_rate >= 0.2:
    #         ga_ppl.evolve_rate -= 0.01

    #     if max_count >= 50 and ga_ppl.mutation_rate <= 0.9:
    #         ga_ppl.mutation_rate += 0.01

    #     print('当前种群总数: {}'.format(len(ppl_left)))
    #     print('淘汰种群数: {}'.format(len(ppl_dead)))
    #     print('当前最优适应度: {}, 个数为: {}'.format(maximum, max_count))
    #     print('当前最低适应度: {}'.format(minimum))
    #     print('当前的阈值为: {:.2f}'.format(threshold))
    #     print('当前的进化率: {:.2f}'.format(ga_ppl.evolve_rate))
    #     print('当前的变异率: {:.2f}'.format(ga_ppl.mutation_rate))

    #     DNA = ga_ppl.get_DNA(address='output.csv')
    #     gen += 1
    #     if len(DNA) == ga_ppl.output_size:
    #         break

    # for dna in DNA:
    #     print(ga_ppl.get_fitness(dna), dna)

    # --------------- READ OUTPUT ---------------
    # output_address = 'output2.csv'
    # read_output(output_address)

    # TODO:
    #  BUG:会在DNA中出现重复的核苷酸，出现的原因来自于crossover的过程
    #  crossover里没有判断是否出现重复的核苷酸
    #  解决方案1：杀死有重复核苷酸的DNA
    #  解决方案2：改变通过rule判断的方式
    #  *** 依然没有处理多面手的问题 ***
    #  BUG：种群数会在某一时刻骤减
    #  出现种群数骤减的原因是由于不断上升的进化率
    #  但是种群中却没有进化出更好的个体
    #  BUG: 种群最后只剩下1个个体，导致种群绝育
    #  其实本质和上一个bug是一样的，主要在于如何控制evolve_rate
    # TODO:
    #  给crossover和mutate进行改进，优化交叉和变异的过程
    #  使得优化和变异的效率得到提升，交叉的过程优先学习那些能提升fitness的变交叉过程
    #  变异也是一样的，这里就需要存储那些使fitness增加的crossover和mutate
