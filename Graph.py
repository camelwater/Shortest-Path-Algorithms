from DijkNode import Dijk_Node
from A_Star_Node import A_Node
from Node import Node
from typing import List
from Algorithm import Algorithm
import random as rand
import numpy as np

class Graph:
    def __init__(self, rows, cols, algo, allow_diagonal=False):
        self.num_rows = rows
        self.num_cols = cols
        self.algo = algo
        self.allow_diagonal = allow_diagonal
        self.graph = self.construct_graph()
        # self.set_up_neighbors()

    def get(self):
        return self.graph
    
    def construct_graph(self) -> List[List[Node]]:
        graph = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        # graph = np.zeros(shape=(self.num_rows, self.num_cols)).tolist()
        counter = 1
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.algo == Algorithm.DIJKSTRA:
                    node = Dijk_Node(r, c, counter)
                else:
                    node = A_Node(r, c, counter)

                graph[r][c] = node
                counter+=1

        return graph
    
    def set_up_neighbors(self):
        for r in range(len(self.graph)):
            for c in range(len(self.graph[r])):
                self.find_neighbors(self.graph[r][c])
    
    def generate_rand_obstacles(self):
        rand_x = rand.sample(range(self.num_rows), int(self.num_rows/2))
        rand_y = rand.sample(range(self.num_cols), int(self.num_cols/2))
        for r, c in zip(rand_x, rand_y):
            print(r, c)
            self.graph[r][c].set_obstacle()

    def find_neighbors(self, node: Node):
        if node.y > 0:
            try:
                node.add_neighbor(self.graph[node.x][node.y-1])
            except IndexError: pass
        
        try:
            node.add_neighbor(self.graph[node.x+1][node.y])
        except IndexError: pass

        try:
            node.add_neighbor(self.graph[node.x][node.y+1])
        except IndexError: pass

        if node.x > 0:
            try:
                node.add_neighbor(self.graph[node.x-1][node.y])
            except IndexError: pass
        
        if self.allow_diagonal:
            if node.x > 0 and node.y > 0:
                try:
                    node.add_neighbor(self.graph[node.x-1][node.y-1])
                except IndexError: pass

            if node.y > 0:
                try:
                    node.add_neighbor(self.graph[node.x+1][node.y-1])
                except IndexError: pass
            
            try:
                node.add_neighbor(self.graph[node.x+1][node.y+1])
            except IndexError: pass

            if node.x > 0:
                try:
                    node.add_neighbor(self.graph[node.x-1][node.y+1])
                except IndexError: pass

        
