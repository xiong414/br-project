Encoding Part:
    Encoding Objects: Every Employees (P,D,F,B,T)
    e.g.: P:[6,2,4,7,8,3,5] represent the sequence list for P,
    then the constraints limit the order.
    the position 0 and 1 have to be 2 or 6.
    the position 2 and 3 have to be

vector:
[2.1: (order, time), 2.3, 2.4, 2.5, 3.1, 3.2,... ,7.5 ,8.1, 8.2, 8.3, 8.4, 8.5]
(The values of each index are continuous, representing the work time.)

这样不能体现出谁和谁是在同时工作的，而谁又在待命中

e.g.: 2 and 6 are not interdependence

1: [2, 0.5], [6, 0.5]
2: [6, 0.5]
3: [6, 6.5], [2, 0.5]
4: [6, 7.5], [2, 1]
5: [6, 1], [2, 1]

dependence:
2.1 -> 2.4 -> 2.3 -> 2.5

6.1
6.2 -> 6.3
    -> 6.4 -> 6.5

segmentation rule:
Depend on the available mission which costs minimum time and still has back-dependence.

total: 10.5

2  [1, 4, 3, 5, 0]
6 [[1, 0, 0, 0, 0],
   [2, 3, 0, 0, 0],
   [2, 4, 5, 0, 0]]


dependence matrix(outer):
[2, 4, 3]
[2, 7, 3]
[6, 4, 3]
[6, 7, 3]
[6, 7, 8, 5]

dependence matrix(inner):
2 [1, 4, 3, 5, 0]
3 [1, 2, 4, 3, 5]
4 [1, 2, 4, 5, 0]
5 [[1, 4, 3, 0, 0],
   [2, 3, 0, 0, 0],
   [5, 0, 0, 0, 0]]
6 [[1, 0, 0, 0, 0],
   [2, 3, 0, 0, 0],
   [2, 4, 5, 0, 0]]
7 [[1, 2, 3, 5, 0],
   [4, 0, 0, 0, 0]]
8 [[1, 0, 0, 0, 0],
   [2, 0, 0, 0, 0],
   [3, 0, 0, 0, 0],
   [4, 0, 0, 0, 0],
   [5, 0, 0, 0, 0]]

Difficulty:
    Encoding the DNA: time is continuous
    Constraint (Dependence): order and time
        order: order值一定要大于它的依赖
        time: time值之和一定要等于"约束值"



#####################################################
#####################################################

2,4,3
2,7,3
6,4,3
6,7,3
6,7,8,5

#####################################################


2, 1, 4, 3, 5, 0
2, 2, 0, 0, 0, 0
3, 1, 2, 4, 3, 5
4, 1, 2, 4, 3, 5
5, 1, 4, 3, 0, 0
5, 2, 3, 0, 0, 0
5, 5, 0, 0, 0, 0
6, 1, 0, 0, 0, 0
6, 2, 3, 0, 0, 0
6, 2, 4, 5, 0, 0
7, 1, 2, 3, 5, 0
7, 4, 0, 0, 0, 0
8, 1, 0, 0, 0, 0
8, 2, 0, 0, 0, 0
8, 3, 0, 0, 0, 0
8, 4, 0, 0, 0, 0
8, 5, 0, 0, 0, 0


#####################################################
#####################################################

SOLUTIONS:

当前最优适应度: 57.5
最优的种群为: 
1 [2, 6, 7, 4, 8, 3, 5]
2 [6, 2, 7, 4, 8, 3, 5]
3 [2, 6, 7, 4, 8, 3, 5]
4 [2, 6, 7, 4, 8, 3, 5]
5 [2, 6, 7, 4, 8, 3, 5]

最优的种群为: 
1 [2, 6, 7, 4, 8, 3, 5]
2 [6, 2, 7, 4, 8, 3, 5]
3 [2, 6, 7, 4, 8, 3, 5]
4 [2, 6, 7, 4, 8, 3, 5]
5 [2, 6, 7, 8, 4, 5, 3]


#####################################################
#####################################################


1, 2, 4, 3
1, 2, 4, 5
1, 2, 7, 3
1, 2, 7, 8, 5
1, 6, 4, 3
1, 6, 7, 3
1, 6, 7, 8, 5
1, 9, 5
10, 12, 15, 19
10, 12, 16, 19
10, 13, 16, 19
10, 12, 16, 20
10, 12, 17, 20
10, 13, 16, 20
10, 13, 17, 20
11, 12, 15, 19
11, 12, 16, 19
11, 13, 16, 19
11, 13, 16, 20
11, 13, 17, 20
11, 14, 17, 20
11, 14, 18, 20


#####################################################
#####################################################


1, 1, 2, 5, 0
1, 1, 3, 5, 0
1, 4, 2, 5, 0
1, 4, 3, 5, 0
2, 1, 4, 5, 0
2, 1, 4, 3, 5
2, 2, 3, 5, 0
3, 1, 2, 3, 5
3, 4, 3, 5, 0
4, 1, 2, 3, 0
4, 1, 2, 4, 5
5, 1, 4, 3, 0
5, 1, 4, 5, 0
5, 2, 5, 0, 0
6, 1, 0, 0, 0
6, 2, 3, 0, 0
6, 2, 4, 5, 0
7, 1, 2, 4, 0
7, 3, 5, 0, 0
8, 1, 0, 0, 0
8, 2, 0, 0, 0
8, 3, 0, 0, 0
8, 4, 0, 0, 0
8, 5, 0, 0, 0
9, 1, 2, 5, 0
9, 1, 3, 5, 0
9, 1, 4, 5, 0
10, 1, 3, 5, 0
10, 2, 4, 5, 0
11, 1, 3, 0, 0
11, 1, 4, 0, 0
11, 2, 4, 0, 0
11, 2, 5, 0, 0
12, 1, 4, 5, 0
12, 2, 3, 0, 0
13, 1, 0, 0, 0
13, 2, 3, 4, 0
13, 5, 0, 0, 0
14, 1, 2, 0, 0
14, 3, 0, 0, 0
14, 4, 5, 0, 0
15, 1, 2, 0, 0
15, 3, 0, 0, 0
15, 4, 0, 0, 0
15, 5, 0, 0, 0
16, 1, 2, 0, 0
16, 1, 3, 0, 0
16, 1, 4, 0, 0
16, 1, 5, 0, 0
17, 1, 5, 0, 0
17, 2, 5, 0, 0
17, 3, 5, 0, 0
17, 4, 5, 0, 0
18, 1, 4, 5, 0
18, 2, 4, 5, 0
18, 3, 4, 5, 0
19, 1, 3, 0, 0
19, 2, 3, 0, 0
19, 5, 4, 0, 0
20, 1, 0, 0, 0
20, 2, 0, 0, 0
20, 3, 0, 0, 0
20, 4, 0, 0, 0
20, 5, 0, 0, 0


############################################################################

DNA=[11, 1, 6, 10, 9, 2, 13, 14, 12, 15, 16, 4, 17, 7, 18, 19, 8, 5, 3, 20]
