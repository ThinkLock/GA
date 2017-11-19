

class Individual(object):
    def __init__(self):
        self.fitness = 0
        self.tac_dic = {}

    def init_origin_ta(self, cell_list):
        self.tac_dic = gen_tac_dic(cell_list)


def gen_tac_dic(cell_list):
    res_dic = {}
    for cell_id, content in cell_list.items():
        res_dic[cell_id] = content[1]
    return res_dic
