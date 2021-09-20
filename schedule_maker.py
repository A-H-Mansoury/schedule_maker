import pandas as pd
import numpy as np
from itertools import combinations
import sys
import os

num = 3
my_courses = ['1718217', '1912296' ,'2410171']

def get_my_courses(lst, df):
    global my_courses, num
    if type(lst) == type([]):
        my_courses = lst
        num = len(lst)
    return run(df)

def a(x):
  return  x.split('_')[0]

def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if len(a_set.intersection(b_set)) > 0:
        return True 
    return False 

def time_intersection(s1, e1, s2, e2):
    s1 = [int(i) for i in s1.split(':')]
    s2 = [int(i) for i in s2.split(':')]
    e1 = [int(i) for i in e1.split(':')]
    e2 = [int(i) for i in e2.split(':')]
    if s1[0] <= s2[0] and s2[0] < e1[0]:
        return 1
    if e1[0] == s2[0] and s2[1] < e1[1]:
        return 1
    if s2[0] <= s1[0]and s1[0] < e2[0]:
        return 1
    if e2[0] == s1[0] and s1[1] < e2[1]:
        return 1
    if s1 == s2 and e1 == e2:
        return 1
    else:
        return 0

def run(df):
    global my_courses, num

    all_courses = dict()
    droped_df = df.drop(['id'], axis=1)

    for id, rw in zip(df['id'], droped_df.to_dict('records')):
        all_courses[id] = rw

    ids = all_courses.keys()

    temp = []
    for id in ids:
        if id[:7] in my_courses:
            temp.append(id)
    ids = temp

    ac = combinations(ids,num)
    result = []

    for sc in ac:     
        if num == len(set(x.split('_')[0] for x in sc)):
            result.append(sc)

    result2 = []

    for res in result:
        flag = True
        for id1,id2  in combinations(res,2):
            if common_member(eval(all_courses[id1]['days']),eval(all_courses[id2]['days'])):
                if time_intersection(all_courses[id1]['Start_time'] ,all_courses[id1]['end_time'],all_courses[id2]['Start_time'] ,all_courses[id2]['end_time']):
                    flag = False
        if flag:  
            result2.append(res)

    return result2
