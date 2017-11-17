# -*- coding: utf-8 -*-
from utils import *


def main():
    cell_list = gen_cell_from_csv('./data/tbCellNew.csv')
    hand_over_count = gen_hoat_matrix('./data/tbHandOverCount.csv')
    adj_dic = gen_adj_matrix('./data/tbAdjCell.csv')


if __name__ == '__main__':
    # 这就是我们的主函数
    main()
