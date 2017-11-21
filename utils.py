# -*- coding: utf-8 -*-
import csv
import random as rd
from sector import Sector
import numpy as np


# 生成小区数据, 随机产生了u值和 寻呼量，
# !!!!!!!!!不要随便运行!!!!!!!!!!!
def random_cell_data(file_path):
    save_file = open('./data/tbCellNew.csv', 'w')
    with open(file_path, 'r') as file:
        data = csv.reader(file.readlines())
        for item in data:
            # sectorid, enodebid, tac, lon ,lat, u , paging
            # 这个地方呀，他就是生成ui的随机值
            u = rd.randint(10, 30)
            paging = u * rd.randint(1, 5)
            save_file.write("{},{},{},{},{},{},{}\n".format(item[3], item[5], item[11], item[13], item[14], u, paging))


# 在csv文件中读取小区数据
def gen_cell_from_csv(file_path):
    cell_list = {}
    with open(file_path, 'r') as line:
        data = csv.reader(line.readlines())
        for item in data:
            # sectorid, enodebid, tac, lon ,lat, u , paging
            cell_list[item[0]] = [item[1], item[2], item[3], item[4], item[5], item[6]]
    return cell_list


# 在csv文件中读取我们的切换次数
def gen_hoat_matrix(file_path):
    res_dic = {}
    with open(file_path, 'r') as line:
        data = csv.reader(line.readlines())
        for item in data:
            if item[2] in res_dic:
                res_dic[item[2]][item[3]] = int(item[4])
            else:
                res_dic[item[2]] = {}
    return res_dic


# 在csv文件中读取小区的邻接关系
def gen_adj_matrix(file_path):
    res_dic = {}
    with open(file_path, 'r') as line:
        data = csv.reader(line.readlines())
        for item in data:
            if item[0] in res_dic:
                res_dic[item[0]].append(item[1])
            else:
                res_dic[item[0]] = []
    return res_dic


# 过滤小区
def filter_cell(cell_list, hand_ober_count, cells):
    res = {}
    res_cells = []
    end_list = []
    index = 0
    for cell_id, content in cell_list.items():
        if cell_id in hand_ober_count:
            res[cell_id] = content
            res_cells.append(cells[int(content)])
            res[cell_id] = index
            index += 1
            end = hand_ober_count[cell_id]
            for item in end.keys():
                if item not in end_list:
                    end_list.append(item)
    # for cell_id, content in cell_list.items():
    #     if cell_id in end_list and cell_id not in res:
    #         res[cell_id] = content
    #         res_cells.append(cells[int(content)])
    #         res[cell_id] = index
    #         index += 1
    return res, res_cells


def convert_hand_over(hand_over, cell_list):
    res = []
    for i, content in cell_list.items():
        item = []
        for j, c in cell_list.items():
            hij = (hand_over[i][j] if j in hand_over[i].keys() else 0) if i in hand_over.keys() else 0
            item.append(hij)
        res.append(item)
    return res

def convert_adj(adj, cell_list):
    res = []
    for i, content in cell_list.items():
        item = []
        for j, c in cell_list.items():
            hij = (1 if j in adj[i] else 0) if i in adj.keys() else 0
            item.append(hij)
        res.append(item)
    return res


def gen_data_from_csv(cell_path, hov_path, adj_path):
    # 在csv文件中读取小区数据
    cell_list = {}
    cells = []
    with open(cell_path, 'r') as line:
        data = csv.reader(line.readlines())
        for index, item in enumerate(data):
            # sectorid, enodebid, tac, lon ,lat, u , paging
            cells.append([item[0], item[1], item[2], item[3], item[4], item[5], item[6]])
            cell_list[item[0]] = index
    hoat_dic = gen_hoat_matrix(hov_path)
    adj_dic = gen_adj_matrix(adj_path)
    #  过滤，生成索引和数组
    cell_list, cells = filter_cell(cell_list, hoat_dic, cells)
    # 生成方便索引的二维数组，切换值
    hand_over = np.array(convert_hand_over(hoat_dic, cell_list))
    adj_matrix = np.array(convert_adj(adj_dic, cell_list))
    return cell_list, cells, hand_over, adj_matrix
