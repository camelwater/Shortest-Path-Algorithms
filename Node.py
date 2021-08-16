from typing import List

class Node:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.neighbors: List[Node] = []
        self.obstacle = False
        self.prev = None

    def set_obstacle(self):
        self.obstacle = True
    
    def is_obstacle(self):
        return self.obstacle
    
    def add_neighbor(self, node):
        self.neighbors.append(node)

    def get_neighbors(self):
        return self.neighbors
    
    def get_prev(self) -> 'Node':
        return self.prev

    def __eq__(self, o: object):
        try:
            return self.id == o.id
        except AttributeError:
            return False
    
    def __hash__(self):
        return hash((self.__class__, self.id))

    def __str__(self):
        return f"{self.id}: ({self.x}, {self.y})"
