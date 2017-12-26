from __future__ import print_function
from __future__ import division

import math
import os
import sys
#from numpy import linalg #eigenvalue vector

#--------------------------Handle train data-------------------------------

file_dir = os.path.dirname(__file__)
train_file_name='/train.csv'
#train_file_name=raw_input()
fp = open(file_dir + train_file_name, "r")
#fp = open('train.csv', "r")
lines = fp.readlines()
fp.close()

# 0:index 1:name 2~10:nine attr 11:class
train_data = []

for i in lines:
    l = i.split(',')
    train_data.append(l)
# median of nine attribute
median = []
tmp = []
for i in train_data:
    for j in range(9):
        tmp.append([])
        tmp[j].append(i[j + 2])

for i in tmp:
    i.sort()
for i in range(9):
    median.append(tmp[i][150])

#--------------------------Handle test data-------------------------------

test_file_name='/test.csv'
#test_file_name=raw_input()
fp2 = open(file_dir + test_file_name, "r")
#fp2 = open('test.csv', "r")
lines = fp2.readlines()
fp2.close()

test_data = []

for i in lines:
    l = i.split(',')
    test_data.append(l)

#--------------------------Create KD Tree-------------------------------

class Node:

    @property
    def data(self):
        return self.data

    @data.setter
    def data(self, data):
        self.data = data

    @property
    def level(self=2):
        return self.level

    @level.setter
    def level(self, level):
        self.level = level

    @property
    def left(self):
        return self.left

    @property
    def right(self):
        return self.right

    def __init__(self, data=[], level=2, left=None, right=None):
        self.data = data  # store train data
        self.level = level  # use which attr to compare
        self.right = right
        self.left = left

    def add_data(self, d):
        self.data.append(d)

    @property
    def children(self):
        if self.left and self.left.data is not None:
            yield self.left, 0
        if self.right and self.right.data is not None:
            yield self.right, 1

    def set_child(self, index, child):
        if index == 0:
            self.left = child
        else:
            self.right = child

    def print_node(self):
        print('Level : ', self.level)
        print('-------------------------------------------------')
        for i in self.data:
            print(i[0])
        print('-------------------------------------------------')


class Kdtree:

    def __init__(self, root=Node([], 2, None, None)):
        self.root = root
        for i in train_data:
            if(i[0] != 'index'):
                 self.root.add_data(i)

    def root(self):
        return self.root

    def add(self, n):
        t = self.root
        while t and t.level < 10:
            tmp = Node([], t.level + 1, None, None)
            if(n[t.level] >= median[t.level - 2]):
                if t.right == None:
                    t.set_child(1, tmp)
                t = t.right
                t.add_data(n)
            else:
                if t.left == None:
                    t.set_child(0, tmp)
                t = t.left
                t.add_data(n)

    def create_empty_tree(self, t):
        cur_level = t.level
        if (cur_level < 10):
            cur_level += 1
            tmp = Node([], cur_level, None, None)
            t.set_child(1, tmp)
            t.set_child(0, tmp)
            self.create(t.right)
            self.create(t.left)

    def print_tree(self, n):
        if not n:
            print('Done.')
        else:
            # inorder
            if n.level == 10:
                n.print_node()
            if n.right:
                self.print_tree(n.right)

            if n.left:
                self.print_tree(n.left)

kd = Kdtree()
for n in train_data:
    if(n[0] != 'index'):
        kd.add(n)
#kd.print_tree(kd.root)

#--------------------------K NN Algo-------------------------------


def Dist(test, find):
    tmp = 0.0
    for i in range(2, 11):
        tmp += ((float)(test[i]) - (float)(find[i])) * \
            ((float)(test[i]) - (float)(find[i]))
    return math.sqrt(tmp)


def search_route(n):
    route = []
    t = kd.root
    while t and t.level < 10:
        if(n[t.level] >= median[t.level - 2]):
            t = t.right
            route.append(1)
        else:
            t = t.left
            route.append(0)
    return route


def find_match(k, test):
    route = search_route(test)
    t = kd.root
    parent = kd.root  # record last one
    for i in route:
        if len(t.data) - 1 > k:
            if(i == 0):
                parent = t
                t = t.left
            else:
                parent = t
                t = t.right
        else:
            t = parent  # if not enough, back to parent node
            break

    pair = []
    for i in t.data:
        pair.append((Dist(test, i), i[0]))
    pair.sort()
    re=[]
    for i in range(k):
        re.append(pair[i][1])
    
    return re

def cal_accu(re,test):
    correct=0
    for i in re:
        if(train_data[(int)(i)+1][11]==test[11]):
            correct+=1
    accu=0.0
    accu=correct/len(re)
    #print("Accuracy: %f" %(accu))
    return accu

output_file_name='/output.txt'
fout = open(file_dir + output_file_name, "w")
k_nn_list=[1,5,10,100]
for i in k_nn_list:
    knn_accu=0
    r=[]
    for j in range(1,4):
        r.append(find_match(i, test_data[j]))
        knn_accu+=cal_accu(r[j-1],test_data[j])
    knn_accu/=3
    fout.write("KNN accuracy: %f\n" %(knn_accu))
    
    for l in r[0]:
        fout.write(l)
        fout.write(' ')
    fout.write('\n')

    for l in r[1]:
        fout.write(l)
        fout.write(' ')
    fout.write('\n')

    for l in r[2]:
        fout.write(l)
        fout.write(' ')
    fout.write('\n\n')

fout.close()
