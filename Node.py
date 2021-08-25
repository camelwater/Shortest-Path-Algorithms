from abc import abstractmethod
from typing import List

class Node:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.neighbors: List[Node] = []
        self.obstacle = False #whether this node is accessible or not
        self.prev = None #the node from which this node came from on the shortest path
        self.inserted = 0 #insertion number into the open set (used to break ties - recent insertions are prioritized)

    def set_obstacle(self):
        self.obstacle = True
    
    def is_obstacle(self):
        return self.obstacle
    
    def add_neighbor(self, node: 'Node'):
        if not self.is_obstacle() and not node.is_obstacle():
            self.neighbors.append(node)

    def get_neighbors(self):
        return self.neighbors
    
    def get_prev(self) -> 'Node':
        return self.prev
    
    def insertion_rank(self):
        return self.inserted

    def clear(self):
        self.inserted = 0
        self.prev = None
        self.neighbors = []

    def __eq__(self, o: object):
        try:
            return self.id == o.id
        except AttributeError:
            return False
            
    @abstractmethod
    def __lt__(self, o: object):
        pass
    
    def __hash__(self):
        return hash((self.__class__, self.id))

    def __str__(self):
        return f"{self.id}: ({self.x}, {self.y})"
