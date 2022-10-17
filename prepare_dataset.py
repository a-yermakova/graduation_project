""" Script helping with extraction of necessary information from dataset."""

import os
import json
import pickle
from torch import zeros


class EnterpriseModel:
    """
    **Класс для хранения информации о модели из JSON-файла.**

    *Attributes:*
    :param a: something
    :type a: int


    ids_of_all_childshapes: list
    список, хранящий индексы всех дочерних фигур

    arrows_directions: list[list]
    список, хранящий айди фигур, к которым направляются стрелки

    final_dataset: list
    итоговый список - датасет, состоящий из матриц смежности для каждой модели

    *Methods:*

    collect_all_ids_and_arrows(self, next_list):
    Проходит по всему JSON файлу, собирая ids всех дочерних фигур и фигур, связанных с ними
    """
    ids_of_all_childshapes: list = []
    arrows_directions: list = []
    final_dataset: list = []

    def __init__(self, model: dict) -> None:
        """
        :param model: модель предприятия, представленная в виде JSON-файла
        :type model: dict
        """
        if model['childShapes']:
            self.collect_all_ids_and_arrows(model['childShapes'])
        # создаем шаблон для матрицы смежности графа модели
        self.adj_matrix = zeros(m_size, m_size)
        for i in range(0, len(self.arrows_directions), 1):
            for j in range(0, len(self.arrows_directions[i]), 1):
                for k in range(0, len(self.ids_of_all_childshapes), 1):
                    # если какой-либо айди в arrows_directions совпадает с айди какой-то фигуры,
                    # то следует обозначить их пересечение в матрице смежности поставив 1
                    if self.arrows_directions[i][j] == self.ids_of_all_childshapes[k]:
                        self.adj_matrix[k][i] = 1
        self.final_dataset.append(self.adj_matrix)
        # после добавления полученной матрицы смежности в final_dataset, очищаем остальные списки за ненадобностью
        self.ids_of_all_childshapes.clear()
        self.arrows_directions.clear()

    def collect_all_ids_and_arrows(self, next_list: list[dict]) -> None:
        for childShape in range(0, len(next_list), 1):
            # заносим в список айди всех фигур, которые есть в модели
            self.ids_of_all_childshapes.append(next_list[childShape]['resourceId'])
            self.arrows_directions.append([])
            # проверяем, связана ли фигура с другими
            if len(next_list[childShape]['outgoing']):
                # если связана, то достаем айди связанной фигуры и заносим его в список
                for connector in range(0, len(next_list[childShape]['outgoing']), 1):
                    self.arrows_directions[len(self.ids_of_all_childshapes) - 1].\
                        append(next_list[childShape]['outgoing'][connector]['resourceId'])
            else:
                # если фигура не связана ни с одной другой, то вместо айди связанной фигуры
                # в список заносим 0
                self.arrows_directions[len(self.ids_of_all_childshapes) - 1].append(0)
        if next_list[childShape]['childShapes']:
            self.collect_all_ids_and_arrows(next_list[childShape]['childShapes'])

# размерность матрицы - наибольшее количество дочерних фигур в модели
m_size = 100

for filename in os.listdir('json'):
    with open(os.path.join('json', filename), 'r') as f:
        model = json.load(f)

# после перебора всех файлов в наборе данных сохраняем полученный датасет как файл .pickle
with open('ds100.pickle', 'wb') as f:
    pickle.dump(EnterpriseModel.final_dataset, f)













