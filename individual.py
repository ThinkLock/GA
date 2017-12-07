class Individual(object):
    def __init__(self):
        self.fitness = 0
        self.tac_dic = {}

    def init_origin_ta(self, cell_list, cell_info):
        self.tac_dic = gen_tac_dic(cell_list, cell_info)

    def init_old_data(self, cell_list):
        self.tac_dic = gen_old_date(cell_list)

    def __str__(self):
        return "{},{}".format(self.fitness, self.tac_dic)


def gen_tac_dic(cell_list, cell_info):
    res_dic = {}
    for cell_id, content in cell_list.items():
        res_dic[cell_id] = int(cell_info[int(content)][2])
    return res_dic


def gen_old_date(cell_list):
    res_dic = {}
    for cell_id, content in cell_list.items():
        res_dic[cell_id] = content[1]
    return res_dic
