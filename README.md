# BR项目开发计划(BR-Project)
## 主函数(Main) main.py
该主函数中包含了默认的三个输入样例，分别针对“一工一人”，“一工多人”，“多面手”问题。然后通过设定问题路径(quest_address)。可调参数有初始种群数目(ppl_size)，迭代次数(generation_max)，变异率(mutation_rate)，进化率(evolve_rate)，游走步长(walker_step)。

设定好上述参数后即可初始化模型，在初始化模型时同时进行了初始化种群和初始化问题。
建立好模型之后，进入迭代步骤。在最大迭代次数的限制下，进行种群迭代。在达到最大迭代次数之后，将返回最佳种群的结构和最佳种群的求解过程。

The main function contains three default input examples for the "one worker", "many workers" and "multi work(Full Stack Developer)" problems. Next, the main function needs to set the question path (quest_address). The adjustable parameters are the initial population size (ppl_size), the number of iterations (generation_max), the mutation rate (mutation_rate), the evolution rate (evolve_rate), and the 
random walk step(walker_step).

After setting the above parameters, the model can be initialized, and the initialization of the population and the initialization problem are performed at the same time when the model is initialized.
After the model is built, the iteration step is entered. Under the limit of the maximum number of iterations, the population is iterated. After the maximum number of iterations is reached, the structure of the best population and the solution procedure for the best population is returned.

## 遗传算法模型(Genetic Algorithm Model) genetic_algorithm.py
该模型在初始化时，需要输入初始种群数目(ppl_size)，迭代次数(generation_max)，变异率(mutation_rate)，进化率(evolve_rate)，游走步长(walker_step)；在模型初始化时，同时初始化模型需要处理的“问题”，以及由问题生成对应路径(path)，以及初始化种群。

在初始化“模型问题”中，先读取两个“问题”文件，分别为outer_module和inner_module。再通过上述文件，生成这个问题所有的从头到尾的路径，用以判断生成的种群是否符合问题的规则。

在初始化种群的过程中，每生成一个种群，需要对路径进行一次检验，种群生成的前提也是按照规则进行随机初始化。

初始化结束后，对种群进行随机分组，在两个组内按照适应度(fitness)大小进行选择，进行下一步交叉(cross over)生成新的个体(child)。新生成的个体可能存在不符合规则的情况，那么就将其舍弃。经过测试，如果工作序列(即问题中的工作数量)越大，那么越容易出现“淘汰新生儿”的情况。

再对新生成的个体进行变异，变异的过程有两种方法。第一种为“核酸交换”(nucleotide exchange)：对一段DNA中的不同位点进行互换。第二种为“DNA交换”(DNA exchange)：对一个种群中的不同员工(employee)的DNA进行互换。两种变异方法均会产生变异个体死亡的情况。第二种方法针对简单问题以及“一工一人”具有较高的“变异存活率”。

最后将生成的新个体与原有个体进行结合，再在所有种群中，按照阈值限制(进化率限制)，淘汰掉部分适应度较高的个体。

以上过程即是单次迭代的过程，再迭代次数限制下，将按照上述过程进行多次迭代。最终求得种群中适应度(fitness)最小的个体。该个体即为最优个体，但并不意味着这个个体就是该问题的最优解，因为遗传算法的劣势，该模型只能保证在迭代的过程中，不断的趋近最优解，但不能确保一定是最优解。

The model needs to enter the initial population number (ppl_size), number of iterations (generation_max), mutation rate (mutation_rate), evolution rate (evolve_rate), and walker step (walker_step) when the model is initialized, and at the same time initialize the model to handle the The "problem", the path generated from the problem, and the initialized population.

To initialize the "model problem", read the two "problem" files, outer_module and inner_module, and then generate all the paths of the problem from beginning to end from these files. Whether the generated populations conform to the rules in question.

During the initialization of the population, the path is checked once for each population generated, and the population is generated on the premise that it is also randomly initialized according to the rules.
After the initialization, the population is randomly grouped into two groups, selected according to fitness, and then crossed over to generate new individuals (children). The newly generated individuals are discarded if they do not conform to the rules. The larger the sequence of jobs (the number of jobs in the problem), the more likely it is that the newborn will be "eliminated".

The newly created individual is then mutated in two ways. The first is a "nucleotide exchange", where different sites in a piece of DNA are swapped. The second is a "DNA exchange" (DNA exchange): the DNA of different employees in a population is exchanged. Both methods of mutation result in the death of the mutated individual. The second method is for simple problems and has a high "mutation survival rate" for "one worker, one employee".

Finally, the new individuals are combined with the existing individuals, and the more adaptable individuals are eliminated from the entire population according to a threshold limit (evolutionary rate limit).

The above process is a single iterative process, and then under the limit of the number of iterations, the above process will be followed for multiple iterations. Finally, the individual with the lowest fitness in the population is found. This individual is the optimal individual, but it does not mean that this individual is the optimal solution to the problem, because of the disadvantages of the genetic algorithm, the model can only ensure that in the process of iterations, and constantly approach the optimal solution, but can not ensure that it must be the optimal solution.

## 工作及员工类(Work and Employees Class) work_object.py
该类中包含了模型中需要使用到的对象。
其中员工类(Employee Class)的初始化条件需要输入一个工作类型(work type)，样例中包含的工作类型有：P, D, F, B, T。在种群初始化的过程中，将对各个员工的DNA进行随机初始化，会根据工作类型进行分配。

工作任务类(Module Class)是继承了int类的一个新类。其属性包含了工作ID(ID)，工作依赖(dependence)，工作时长(time)，工作可执行状态(status)；拥有以下方法，刷新状态：根据依赖(dependence)的改变刷新工作的可执行状态，添加依赖(add_dep)：对工作的依赖进行添加，删除依赖(del_dep)：对工作的依赖进行删除，以上两个方法均会对工作状态(status)进行刷新，添加时间(add_time)：对工作时间进行添加。

员工组类(Group Class)，该类中包含属性：组ID(id)，组内成员(group_list)，以及该组的适应度(fitness)。可以通过“添加员工”(add_employee)方法向组内添加员工。

This class contains the objects to be used in the model.
The initialization conditions of the Employee Class require a work type, and the sample contains the following work types: P, D, F, B, T. During the initialization of the population, the DNA of each employee will be initialized randomly, and will be assigned according to the work type.

The job task class (Module Class) is a new class that inherits the int class. Its properties include job ID, job dependency, job duration, and job executable state; it has the following methods, refresh state: refresh the executable state of the job according to the change of dependency, add dependency (add_dep): add and remove dependency of the job (del_dep): delete the dependency of the job, the above two methods will refresh the status of the job, add time (add_time): add the time of the job.

Employee Group Class, this class contains attributes: group ID(id), group_list, and fitness. You can add employees to the group by using the "add_employee" method.

## 读取文件类(Read File Class) read_file.py
读取文件即对问题的依赖进行读取，最后导入至模型中，用以模型构建以及员工初始化和检验。

The read file reads the problem's dependencies and imports them into the model for model building and staff initialization and verification.



