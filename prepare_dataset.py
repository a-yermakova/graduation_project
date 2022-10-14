import json
import torch
import torch.utils.data
import os
import pickle

m_size = 100


class DataPreparing:
  ids = []
  connectors = []
  dataset = []
  def __init__(self, d1):

    if d1['childShapes']:
      self.list_collector(d1['childShapes'])
    self.adj_matrix = torch.zeros(m_size, m_size)
    for i in range(0, len(self.connectors), 1):
      for j in range(0, len(self.connectors[i]), 1):
        for k in range(0, len(self.ids), 1):
          if self.connectors[i][j] == self.ids[k]:
            self.adj_matrix[k][i] = 1
    self.dataset.append(self.adj_matrix)
    self.ids.clear()
    self.connectors.clear()

  def list_collector(self, next_list):
    for childShape in range(0, len(next_list), 1):
      self.ids.append(next_list[childShape]['resourceId'])
      self.connectors.append([])
      if len(next_list[childShape]['outgoing']):
        for con in range(0, len(next_list[childShape]['outgoing']), 1):
          self.connectors[len(self.ids) - 1].append(next_list[childShape]['outgoing'][con]['resourceId'])
      else: self.connectors[len(self.ids) - 1].append(0)
      if next_list[childShape]['childShapes']:
        self.list_collector(next_list[childShape]['childShapes'])

for filename in os.listdir('json25'):
  with open(os.path.join('json25', filename), 'r') as f:
       d1 = json.load(f)
       data = DataPreparing(d1)

with open('ds25.pickle', 'wb') as f:
    pickle.dump(DataPreparing.dataset, f)
