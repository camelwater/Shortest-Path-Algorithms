from Node import Node
from functools import total_ordering

@total_ordering
class A_Node(Node):
    def __init__(self, x, y, id):
        super().__init__(x, y, id)
        self.f_score = 99999999 #total distance from start to end through this node
        self.g_score = 99999999 #distance from start to this node
    
    def set_fScore(self, score):
        self.f_score = score
    
    def set_gScore(self, score):
        self.g_score = score
    
    def __lt__(self, o: object):
        return (self.f_score, self.inserted) < (o.f_score, o.inserted)
    
    def __repr__(self):
        return f"A*_Node(x:{self.x}, y:{self.y}, id:{self.id}, fScore={self.f_score:.2f})"