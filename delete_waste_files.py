""" Script helping with deletion of unwanted files from dataset in directory. """

import json
import os


class EnterpriseModel:
    """
    **Класс для хранения информации о модели из JSON-файла.**

    *Attributes:*
    ids_of_all_childshapes: list
    список, хранящий индексы всех дочерних фигур

    *Methods:*
    collect_all_ids(self, next_list):
    Проходит по всему JSON файлу, собирая ids всех дочерних фигур
    """
    ids_of_all_childshapes: list=[]

    def __init__(self, model: dict) -> None:
        """
        :param model: модель предприятия, представленная в виде JSON-файла
        :type model: dict
        """
        if model['childShapes']:
            self.collect_all_ids(model['childShapes'])

    def collect_all_ids(self, next_list: list[dict]) -> None:
        """ Проходит по всему JSON файлу, собирая ids всех дочерних фигур

        :param next_list: список дочерних фигур
        :type next_list: list[dict]
        """
        # берем len(next_list), т.к. childShape должно иметь значение int
        for childShape in range(0, len(next_list), 1):
            self.ids_of_all_childshapes.append(next_list[childShape]['resourceId'])
            if next_list[childShape]['childShapes']:
                self.collect_all_ids(next_list[childShape]['childShapes'])


# количество ChildShapes в json файле не должно превышать это значение
shapes_number_limit = 100
# список с именами файлов, которые нужно удалить
filenames_to_delete = []
for filename in os.listdir('json'):
    with open(os.path.join('json', filename), 'r') as f:
        model = json.load(f)
        # если модель из JSON-файла имеет больше дочерних фигур, чем установлено,
        # то этот файл удаляется из папки
        if len(EnterpriseModel(model).ids_of_all_childshapes) > shapes_number_limit:
            filenames_to_delete.append('json/' + filename)
        EnterpriseModel.ids_of_all_childshapes.clear()

for i in filenames_to_delete:
    os.remove(i)