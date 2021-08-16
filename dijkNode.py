from Node import Node
from functools import total_ordering

@total_ordering
class Dijk_Node(Node):
    def __init__(self, x, y, id):
        super().__init__(x, y, id)
        self.dist = 99999999
    
    def set_dist(self, distance):
        self.dist = distance
    
    def __lt__(self, obj):
        return self.dist < obj.dist