# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 13:53:51 2021

@author: student
"""

from collections import defaultdict
import sys
from io import StringIO
import numpy as np
import math

# создание класса точек, где храниться вся информация о них
class Points(object):
    
    def __init__(self,name, coords):
        self.coords = coords  
        self.name = name
        
    def coords(coords):
        coords = int(coords)
        return coords
    def name(name):
        return name
    
# массив со всеми точками
mass = [
        Points('START1', [11, 21]),
        Points('STAR1', [11, 47]),
    	Points('START2', [347, 111]),
        Points('STAR2', [347, 89]),
        #круговой движ
        Points('C25', [36, 60]),
        Points('C26', [64, 60]),
        Points('C27', [80, 50]),
        Points('C21', [80, 27]),
	    Points('C22', [58, 17]),	
        Points('C23', [38, 24]),
        Points('C24', [35, 39]),
        
        Points('C11', [318, 55]),
        Points('C12', [320, 35]),
        Points('C13', [307, 17]),
        Points('C14', [289, 16]),
	    Points('C15', [274, 28]),
        Points('C16', [274, 51]),
        Points('C17', [299, 62]),
        #перекрёстки
        Points('P11', [166, 202]),
        Points('P12', [191, 202]),
        Points('P13', [166, 180]),
        Points('P14', [193, 180]),
        
        Points('P21', [193, 27]),
        Points('P22', [166, 27]),
        Points('P23', [193, 48]),
        Points('P24', [166, 48]),
        #дорога снаружи
        Points('G1', [36, 101]),
        Points('G3', [36, 133]),
        Points('T11', [36, 182]),
        Points('T12', [52, 201]),
        Points('R3', [90, 201]),
        Points('R1', [126, 201]),
        Points('O3', [229, 201]),
        Points('O1', [261, 201]),
        Points('T21', [301, 201]),
        Points('T22', [324, 178]),
        Points('B2', [324, 144]),
        Points('S1', [245, 28]),
        Points('S2', [113, 28]),
        #дорга внутри
        Points('B3', [300, 106]),
        Points('B1', [300, 133]),
        Points('T34', [300, 160]),
        Points('T33', [286, 175]),
        Points('O2', [261, 180]),
        Points('O4', [230, 180]),
        Points('R2', [125, 180]),
        Points('R4', [95, 180]),
        Points('T32', [69, 180]),
        Points('T31', [59, 163]),
        Points('G4', [59, 134]),
        Points('G2', [59, 104]),
        Points('S4', [113, 51]),
        Points('S3', [242, 51]),
        #дорога между
        Points('Y1', [167, 104]),
        Points('Y3', [167, 134]),
        Points('Y4', [192, 134]),
        Points('Y2', [192, 104]),
        #финиши
        Points('F1', [12, 194]),
        Points('F2', [347, 192]),        
        ]  
graph = {
#старты
    'START1': ['STAR1'],
    'STAR1': ['C25'],
	'START2': ['STAR2'],
    'STAR2': ['C11'],
#круговой движ
    'C25': ['G1', 'C26'],
    'C26': ['C27'],
    'C27': ['S4', 'C21'],
    'C21': ['C22'],
	'C22': ['C23'],	
    'C23': ['C24'],
    'C24': ['C25'],

    'C11': ['C12'],
    'C12': ['C13'],
    'C13': ['C14'],
    'C14': ['C15'],
	'C15': ['S1', 'C16'],
    'C16': ['C17'],
    'C17': ['B3', 'C11'],
#перекрёстки
    'P11': ['P12', 'P14'],
    'P12': ['O3'],
    'P13': ['P12', 'R2'],
    'P14': ['P13', 'Y4'],

    'P21': ['P22', 'P24'],
    'P22': ['S2'],
    'P23': ['P22', 'S3'],
    'P24': ['P23', 'Y1'],
#дорога снаружи
    'G1': ['G3'],
    'G3': ['T11'],
    'T11': ['T12'],
    'T12': ['F1', 'R3'],
    'R3': ['R1'],
    'R1': ['P11'],
    'O3': ['O1'],
    'O1': ['T21'],
    'T21': ['F2', 'T22'],
    'T22': ['B2'],
    'B2': ['C11'],
    'S1': ['P21'],
    'S2': ['C21'],
#дорга внутри
    'B3': ['B1'],
    'B1': ['T34'],
    'T34': ['T33'],
    'T33': ['O2'],
    'O2': ['O4'],
    'O4': ['P14'],
    'R2': ['R4'],
    'R4': ['T32'],
    'T32': ['T31'],
    'T31': ['G4'],
    'G4': ['G2'],
    'G2': ['C26'],
    'S4': ['P24'],
    'S3': ['C16'],
#дорога между
    'Y1': ['Y3'],
    'Y3': ['P13'],
    'Y4': ['Y2'],
    'Y2': ['P23'],
#финиши
    'F1': ['T12'],
    'F2': ['T21'],
}

# поиск пути
way = []
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
        global path
        path = []

        # Рекурсивный вызов вспомогательной функции печати всех путей
        t = self.printAllPathsUtil(s, d, visited, path)
        return t
    
# исполнение

def my_programm(start, end):
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
    
    #    print(ways)
    
    def find_points(name_start, name_end):
        m = []
        for i in range(0, len(mass)):
            id = mass[i].name
            if id == name_start:
                id_start = i
            if id == name_end:
                id_end = i
        m = [id_start, id_end]
        return m

    little = []
    for i in range(0, len(ways)):
        little.append(len(ways[i]))
    needed_way = []
    if (len(little)):
        needed_way = np.argmin(little)
        needed_way = ways[needed_way]
        print(needed_way)

        for i in range(0, len(needed_way)-1):
            m = find_points(needed_way[i], needed_way[i+1])
            start = mass[m[0]].coords
            end = mass[m[1]].coords
            a = end[0]-start[0]
            b = end[1]-start[1]
            corner = math.atan2(a, b)
            corner = math.degrees(corner)
            lengh = (start[0]-end[0])**2+(start[1]-end[1])**2
            lengh = math.sqrt(lengh)
            current = mass[m[1]].name
            needed_corner = corner - our_corner
            do.append(needed_corner)
            do.append(lengh)

            our_corner = corner

        comands = do
        return comands

#comands = my_programm()
#print(comands)












 
 





    
    


