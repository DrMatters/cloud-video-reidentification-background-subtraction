from features_task.real.utils import compare_structure
import json


def main():
    res = compare_structure.create_relative_walk('D:\\Документы\\Кирилл\\YandexDisk\\Documents\\Sync\\Datasets\\DukeMTMC')
    with open('./res_walk.json', 'w', encoding='utf-8') as res_walk_f:
        json.dump(res, res_walk_f)
    print('success')


if __name__ == '__main__':
    main()
