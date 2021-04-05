# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 13:53:51 2077

@author: я что похож на автора? (author ne_oleg)
"""

from collections import defaultdict
import sys
from io import StringIO
import numpy as np
import math

# данный класс используется для создания точек и хранения информации об их координатах
class Points(object):
    
    def __init__(self,name, coords):
        self.coords = coords  
        self.name = name
        
    def coords(coords):
        coords = int(coords)
        return coords
    def name(name):
        return name
    
# массив, хранящий в себе точки из класса Points
graph_coords = [
        # старты
        Points('START1', [28, 26]),
        Points('STAR1', [28, 102]),
        Points('START2', [770, 265]),
        Points('STAR2', [770, 190]),
        # круговой движение
        Points('D1', [715, 168]),
        Points('C11', [702, 116]),
        Points('C12', [718, 78]),
        Points('C13', [668, 33]),
        Points('C14', [616, 62]),
        Points('C15', [618, 112]),
        Points('C16', [662,136]),

        Points('C21', [83, 116]),
        Points('C22', [132, 132]),
        Points('C23', [180, 112]),
        Points('C24', [182, 62]),
        Points('C25', [132, 33]),
        Points('C26', [83, 63]),
        # перекрёстки
        Points('P11', [373, 447]),
        Points('P12', [422, 447]),
        Points('P13', [373, 390]),
        Points('P14', [420, 390]),

        Points('P21', [422, 62]),
        Points('P22', [374, 62]),
        Points('P23', [422, 112]),
        Points('P24', [372, 112]),
        # дорога снаружи
        Points('G1', [83, 228]),
        Points('G3', [83, 301]),
        Points('T11', [83, 412]),
        Points('T12', [117, 447]),
        Points('R3', [215, 447]),
        Points('R1', [285, 447]),
        Points('O3', [512, 447]),
        Points('O1', [583, 447]),
        Points('T31', [682, 447]),
        Points('T32', [718, 400]),
        Points('B2', [718, 324]),
        Points('S2', [543, 62]),
        Points('S1', [252, 62]),
        # дорга внутри
        Points('S3', [252, 112]),
        Points('S4', [544, 112]),
        Points('B3', [662, 228]),
        Points('B1', [662, 300]),
        Points('T42', [662, 357]),
        Points('T41', [630, 390]),
        Points('O2', [580, 390]),
        Points('O4', [512, 390]),
        Points('R2', [286, 390]),
        Points('R4', [215, 390]),
        Points('T22', [161, 390]),
        Points('T21', [132, 360]),
        Points('G4', [132, 300]),
        Points('G2', [132, 228]),
        # дорога между
        Points('Y1', [373, 228]),
        Points('Y3', [373, 302]),
        Points('Y2', [422, 228]),
        Points('Y4', [422, 303]),
        # финиши
        Points('F11', [25, 448]),
        Points('F12', [25, 395]),
        Points('F21', [768, 447]),
        Points('F22', [768, 391]),
        ]  


# Данный массив хранит в себе теже точки, что и массив graph_coords,
# за одним исключением - в него внесены не координаты, а вершины, до которых можно добраться из каждой конкретной точки графа
graph = {
    # старты
    'START1': ['STAR1'],
    'STAR1': ['C21'],
	'START2': ['STAR2'],
    'STAR2': ['D1'],
    # круговой движ P.S. круговое движение
    'D1': ['C11'],
    'C11': ['C12'],
    'C12': ['C13'],
    'C13': ['C14'],
	'C14': ['S2', 'C15'],
    'C15': ['C16'],
    'C16': ['B3', 'C11'],

    'C21': ['G1', 'C22'],
    'C22': ['C23'],
    'C23': ['S3', 'C24'],
    'C24': ['C25'],
	'C25': ['C26'],
    'C26': ['C21'],
    # перекрёстки
    'P11': ['P12'],
    'P12': ['O3'],
    'P13': ['R2'],
    'P14': ['Y4', 'P13'],

    'P21': ['P22'],
    'P22': ['S1'],
    'P23': ['S4'],
    'P24': ['Y1', 'P23'],
    # дорога снаружи
    'G1': ['G3'],
    'G3': ['T11'],
    'T11': ['T12'],
    'T12': ['F11', 'R3'],
    'R3': ['R1'],
    'R1': ['P11'],
    'O3': ['O1'],
    'O1': ['T31'],
    'T31': ['F21', 'T32'],
    'T32': ['B2'],
    'B2': ['D1'],
    'S2': ['P21'],
    'S1': ['C24'],
    # дорга внутри
    'S3': ['P24'],
    'S4': ['C15'],
    'B3': ['B1'],
    'B1': ['T42'],
    'T42': ['T41'],
    'T41': ['O2'],
    'O2': ['O4'],
    'O4': ['P14'],
    'R2': ['R4'],
    'R4': ['T22'],
    'T22': ['T21'],
    'T21': ['G4'],
    'G4': ['G2'],
    'G2': ['C22'],
    # дорога между
    'Y1': ['Y3'],
    'Y3': ['P13'],
    'Y2': ['P23'],
    'Y4': ['Y2'],
    # финиши
    'F11': ['T12', 'F12'],
    'F12': ['F11'],
    'F21': ['T31', 'F22'],
    'F22': ['F21'],
}

def my_programm(start, end):
    # Здесь, а именно 43 строками ниже, производиться поиск наикротчайшего пути
    # way - хранит путь, а вы хотели услышать что-то иное?
    way = []
    # класс Graph преобразкет наш массив graph и ищет с его помощью наикратчайший путь
    class Graph:

        def __init__(self, vertices):
            # Нет. вершин
            self.V = vertices

            # словарь по умолчанию для хранения графа
            self.graph = defaultdict(list)

        # функция добавления ребра в граф
        def addEdge(self, u, v):
            self.graph[u].append(v)

        '''Рекурсивная функция для печати всех путей от 'u' до 'd'.
        visit [] отслеживает вершины в текущем пути.
        path [] хранит актуальные вершины, а path_index является текущим
        индексом в path[]'''

        def printAllPathsUtil(self, u, d, visited, path):

            # Пометить текущий узел как посещенный и сохранить в path
            visited[list(self.graph.keys()).index(u)] = True
            path.append(u)

            # Если текущая вершина совпадает с точкой назначения, то
            # print(current path[])
            if u == d:
                way.append(path.copy())
            #            print(path)

            else:
                # Если текущая вершина не является пунктом назначения
                # Повторить для всех вершин, смежных с этой вершиной
                for i in self.graph[u]:
                    if visited[list(self.graph.keys()).index(i)] == False:
                        self.printAllPathsUtil(i, d, visited, path)

            # Удалить текущую вершину из path[] и пометить ее как непосещенную
            path.pop()
            visited[list(self.graph.keys()).index(u)] = False
            return way

        # Печатает все пути от 's' до 'd'
        def printAllPaths(self, s, d):

            # Отметить все вершины как не посещенные
            visited = [False] * (self.V)

            # Создать массив для хранения путей
            # global path
            path = []

            # Рекурсивный вызов вспомогательной функции печати всех путей
            way = self.printAllPathsUtil(s, d, visited, path)
            return way

    comands = 0
    our_corner = 0
#    start = 'START1'
#    end = 'G3'
    do = []
    def classes_put(start, end):
        
        g = Graph(len(graph.keys()))
        for i, v in graph.items():
            for e in v:
                g.addEdge(i, e)  
    #    print ("Ниже приведены все различные пути от {} до {} :".format(start, end))
        ways = g.printAllPaths(start, end)
        return ways
    
    ways = classes_put(start, end)
    
    # print(ways)
    # Данная функция совмещает два наших массива, а имменно находит id-шники элементов из массива graph и отдаёт их во власть graph_coords
    def find_points(name_start, name_end):
        for i in range(0, len(graph_coords)):
            id = graph_coords[i].name
            if id == name_start:
                id_start = i
            if id == name_end:
                id_end = i
        m = [id_start, id_end]
        return m
    # Здесь мы находим наикротчайший путь среди тех, что получены от класса Graph
    little = []
    for i in range(0, len(ways)):
        little.append(len(ways[i]))
    needed_way = []
    if little != []:
        needed_way = np.argmin(little)
        needed_way = ways[needed_way]
        print(needed_way)

        #Это переводит наш путь в понятные для человека и робота команды
        for i in range(0, len(needed_way)-1):
            m = find_points(needed_way[i], needed_way[i+1])
            start = graph_coords[m[0]].coords
            end = graph_coords[m[1]].coords
            a = end[0]-start[0]
            b = end[1]-start[1]
            corner = math.atan2(a, b)
            corner = math.degrees(corner)
            lengh = (start[0]-end[0])**2+(start[1]-end[1])**2
            lengh = math.sqrt(lengh)
            current = graph_coords[m[1]].name
            needed_corner = corner - our_corner
            do.append(needed_corner)
            do.append(lengh)

            our_corner = corner

        comands = do
        return comands
    else:
        return None

#comands = my_programm()
#print(comands)












 
 





    
    


















# Thank you Peter XXXelich
    ###########   ###########
 ##############################
################################
 ##############################
  ############################
    #########################
      ####################
          ############
            #######
              ###