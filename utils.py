# -*- coding: utf-8 -*-
import csv
import random as rd
from sector import Sector


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
