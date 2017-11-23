# -*- coding: utf-8 -*-
import csv
from utils import *
import pickle
from individual import Individual
import numpy as np
import copy
import multiprocessing
from config import *

def get_candidate_from_cell(cell_info):
    res = []
    for item in cell_info:
        if int(item[2]) not in res:
            res.append(int(item[2]))
    return res


# 计算适应度的值
def calculate_origin_fitness(idv, hand_over, cell_list, cell_info):
    N = len(idv.tac_dic)
    res = 0.0
    for i in idv.tac_dic.keys():
        for j in idv.tac_dic.keys():
            sij = 0 if idv.tac_dic[i] != idv.tac_dic[j] else 1
            ui = int(cell_info[int(cell_list[i])][5])
            hij = hand_over[cell_list[i]][cell_list[j]]
            res += (cu * hij * (1 - sij) + alpha * cp * ui * sij)
    return res


def calculate_cso(t, hand_over, cell_list, cell_info):
    res = 0.0
    for i in t.keys():
        cell_index_x = cell_list[i]
        ui = int(cell_info[int(cell_index_x)][5])
        for j in t.keys():
            cell_index_y = cell_list[j]
            sij = 0 if t[i] != t[j] else 1
            hij = hand_over[int(cell_index_x)][int(cell_index_y)]
            res += (cu * hij * (1 - sij) + alpha * cp * ui * sij)
    return res


def calculate_b(cell_list, cell_info):
    B = 0
    for cell_id, content in cell_list.items():
        B += int(cell_info[int(content)][5])
    return B


def calculate_bl(t0, tl, cell_list, cell_info):
    B = 0
    for cell_id_i in t0.keys():
        if t0[cell_id_i] != tl[cell_id_i]:
            B += int(cell_info[int(cell_list[cell_id_i])][5])
    return B


def gen_new_individual(t0, tl, candidate, hand_over, cell_list, cell_info, B):
    bl = calculate_bl(t0, tl, cell_list, cell_info)
    cnt = 0
    while True:
        deita_start = 0
        i_start = -1
        t_start = -1

        N_sub = [x for x in tl.keys() if
                 t0[x] != tl[x] or (t0[x] == tl[x] and bl + int(cell_info[int(cell_list[x])][5]) < B)]
        for i in N_sub:
            lambda_sub = [m for m in candidate if
                          (j for j in tl.keys() if tl[j] == m and hand_over[cell_list[i]][cell_list[j]] > 0)]
            lambda_sub.remove(tl[i])
            print(i)
            for m in lambda_sub:
                t_sub = copy.deepcopy(tl)
                t_sub[i] = m
                t1 = calculate_cso(tl, hand_over, cell_list, cell_info)
                t2 = calculate_cso(t_sub, hand_over, cell_list, cell_info)
                if t1 - t2 > deita_start:
                    deita_start = t1 - t2
                    i_start = i
                    m_start = m
        if deita_start > 0:
            if tl[i_start] == t0[i_start]:
                bl = bl + int(cell_info[int(cell_list[i_start])][5])
            else:
                if m_start == t0[i_start]:
                    bl = bl - int(cell_info[int(cell_list[i_start])][5])
            tl[i_start] = m_start
        print(deita_start)
        print(tl)
        with open('./gen1/{}_{}.dat'.format(cnt, deita_start), 'wb') as pos:
            pickle.dump(tl, pos)
        if deita_start == 0:
            break
        cnt += 1

    return tl


def main():
    # 读取数据
    cell_list, cells_info, haot_matrix, adj_matrix = \
        gen_data_from_csv('./data/tbCellNew.csv', './data/tbHandOverCount.csv', './data/tbAdjCell.csv')
    print("优化小区的个数: {}".format(len(cell_list)))

    # 根据原始的TAC分配值，生成跟踪区的候选集
    candidate = get_candidate_from_cell(cells_info)
    print("原始可分配的TAC个数: {}".format(len(candidate)))

    ancestor = Individual()
    ancestor.init_origin_ta(cell_list, cells_info)

    origin_cso = calculate_origin_fitness(ancestor, haot_matrix, cell_list, cells_info)
    print("初始评测值: {}\n".format(origin_cso))

    tl = gen_new_individual(ancestor.tac_dic, ancestor.tac_dic, candidate, haot_matrix, cell_list, cells_info,
                            calculate_b(cell_list, cells_info))
    # print(ancestor.tac_dic)
    # print(tl)


if __name__ == '__main__':
    # 这就是我们的主函数
    main()
