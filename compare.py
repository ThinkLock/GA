import pickle


def compare():
    with open('./gen1/0_29888.4.dat', 'rb') as pos:
        data = pickle.load(pos)
    print(data)
    with open('./gen1/23_8854.5.dat', 'rb') as pos:
        data1 = pickle.load(pos)
    print(data1)
    cnt = 0
    for item,content in data.items():
        if content != data1[item]:
            cnt += 1
            print ("{}:{} --> {}".format(item, content, data1[item]))
    print(cnt)

if __name__ == '__main__':
    compare()