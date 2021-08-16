from Node import Node
from functools import total_ordering

@total_ordering
class A_Node(Node):
    def __init__(self, x, y, id):
        super().__init__(x, y, id)
        self.f_score = 99999999
        self.g_score = 99999999
    
    def set_fScore(self, score):
        self.f_score = score
    
    def set_gScore(self, score):
        self.g_score = score
    
    def __lt__(self, o: object):
        return self.f_score < o.f_score