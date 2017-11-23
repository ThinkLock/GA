# -*- coding: utf-8 -*-
from utils import *
from individual import *
from config import *
import copy
import pickle


# 过滤小区
def filter_cell(cell_list, hand_ober_count):
    res = {}
    end_list = []
    for cell_id, content in cell_list.items():
        if cell_id in hand_ober_count:
            res[cell_id] = content
            end = hand_ober_count[cell_id]
            for item in end.keys():
                if item not in end_list:
                    end_list.append(item)

    # for cell_id, content in cell_list.items():
    #     if cell_id in end_list and cell_id not in res:
    #         res[cell_id] = content
    return res


def get_candidate_from_cell_list(cell_list):
    res = []
    for cell, content in cell_list.items():
        if content[1] not in res:
            res.append(content[1])
    return res


# 去掉重复小区
def remove_repeat(cell_list):
    res = []
    flag = []
    for cell in cell_list:
        if cell.sector_id not in flag:
            res.append(cell)
            flag.append(cell.sector_id)
    return res



# 计算适应度的值
def calculate_origin_fitness(idv, hand_over, cell_list):
    N = len(idv.tac_dic)
    res = 0.0
    for i in idv.tac_dic.keys():
        for j in idv.tac_dic.keys():
            hij = (hand_over[i][j] if j in hand_over[i].keys() else 0) if i in hand_over.keys() else 0
            sij = 0 if idv.tac_dic[i] != idv.tac_dic[j] else 1
            ui = int(cell_list[i][4])
            res += (cu * hij * (1 - sij) + alpha * cp * ui * sij)
    return res


def calculate_cso(t, hand_over, cell_list):
    res = 0.0
    for i in t.keys():
        ui = int(cell_list[i][4])
        for j in t.keys():
            hij = (hand_over[i][j] if j in hand_over[i].keys() else 0) if i in hand_over.keys() else 0
            # hij = get_hij(i, j, hand_over)
            sij = 0 if t[i] != t[j] else 1
            res += (cu * hij * (1 - sij) + alpha * cp * ui * sij)
    return res


def calculate_B(cell_list):
    B = 0
    for cell_id, content in cell_list.items():
        B += int(content[4])
    return B


def calculate_bl(t0, tl, cell_list):
    B = 0
    for cell_id_i in t0.keys():
        if t0[cell_id_i] != tl[cell_id_i]:
            B += int(cell_list[cell_id_i][4])
    return B


def gen_new_individual(t0, tl, candidate, hand_over, cell_list, B):
    bl = calculate_bl(t0, tl, cell_list)
    cnt = 0
    while True:
        deita_start = 0
        i_start = -1
        t_start = -1
        N_sub = [x for x in tl.keys() if t0[x] != tl[x] or (t0[x] == tl[x] and bl + int(cell_list[x][4]) < B)]
        for i in N_sub:
            lambda_sub = [m for m in candidate if (j for j in tl.keys() if tl[j] == m and hand_over[i][j] > 0)]
            lambda_sub.remove(tl[i])
            print(i)
            for m in lambda_sub:
                t_sub = copy.deepcopy(tl)
                t_sub[i] = m
                t1 = calculate_cso(tl, hand_over, cell_list)
                t2 = calculate_cso(t_sub, hand_over, cell_list)
                if t1 - t2 > deita_start:
                    deita_start = t1 -t2
                    i_start = i
                    m_start = m

        if deita_start > 0:
            if tl[i_start] == t0[i_start]:
                bl = bl + int(cell_list[i_start][4])
            else:
                if m_start == t0[i_start]:
                    bl = bl - int(cell_list[i_start][4])
            tl[i_start] = m_start
        print(deita_start)
        print(tl)
        with open('./generation/{}_{}.dat'.format(cnt, deita_start), 'wb') as pos:
            pickle.dump(tl, pos)
        if deita_start == 0:
            break

    return tl


def main():
    cell_list = gen_cell_from_csv('./data/tbCellNew.csv')
    hand_over_count = gen_hoat_matrix('./data/tbHandOverCount.csv')
    adj_dic = gen_adj_matrix('./data/tbAdjCell.csv')

    # 过滤小区，仅仅优化在 切换次数表中存在的小区
    cell_list = filter_cell(cell_list, hand_over_count)
    # cell_list = remove_repeat(cell_list)
    # 目前没有对小区进行过滤选择
    print("优化小区个数：{}\n".format(len(cell_list)))

    # 根据原始的TAC分配值，生成跟踪区的候选集
    candidate = get_candidate_from_cell_list(cell_list)
    print("原始可分配的TAC个数: {}\n".format(len(candidate)))
    print(candidate)

    ancestor = Individual()
    ancestor.init_old_data(cell_list)

    origin_cso = calculate_origin_fitness(ancestor, hand_over_count, cell_list)
    print("初始评测值: {}\n".format(origin_cso))

    tl = gen_new_individual(ancestor.tac_dic, ancestor.tac_dic, candidate, hand_over_count, cell_list,
                            calculate_B(cell_list))
    print(ancestor.tac_dic)
    print(tl)


if __name__ == '__main__':
    # 这就是我们的主函数
    main()
