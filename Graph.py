from dijkNode import Dijk_Node
from A_Star_Node import A_Node
from Node import Node
from typing import List
from Algorithm import Algorithm

class Graph:

    def __init__(self, rows, cols, algo=None):
        self.num_rows = rows
        self.num_cols = cols
        self.algo = algo
        self.graph = self.construct_graph()
    
    def get(self):
        return self.graph
    
    def construct_graph(self) -> List[List[Node]]:
        graph = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        counter = 1
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.algo == Algorithm.DIJKSTRA:
                    node = Dijk_Node(r, c, counter)
                else:
                    node = A_Node(r, c, counter)

                graph[r][c] = node
                counter+=1
        
        for r in range(len(graph)):
            for c in range(len(graph[r])):
                self.find_neighbors(graph[r][c], graph)

        return graph

    def find_neighbors(self, node: Node, graph):
        if node.x > 0 and node.y > 0:
            try:
                node.add_neighbor(graph[node.x-1][node.y-1])
            except IndexError: pass

        if node.y > 0:
            try:
                node.add_neighbor(graph[node.x][node.y-1])
            except IndexError: pass

        if node.y > 0:
            try:
                node.add_neighbor(graph[node.x+1][node.y-1])
            except IndexError: pass
        
        try:
            node.add_neighbor(graph[node.x+1][node.y])
        except IndexError: pass

        try:
            node.add_neighbor(graph[node.x+1][node.y+1])
        except IndexError: pass

        try:
            node.add_neighbor(graph[node.x][node.y+1])
        except IndexError: pass

        if node.x > 0:
            try:
                node.add_neighbor(graph[node.x-1][node.y+1])
            except IndexError: pass

        if node.x > 0:
            try:
                node.add_neighbor(graph[node.x-1][node.y])
            except IndexError: pass
