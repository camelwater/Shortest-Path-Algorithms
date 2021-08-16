from math import floor
from typing import List
from Node import Node

class PriorityQueue:
    '''
    min-heap priority queue
    '''

    def __init__(self):
        '''
        Initialize PriorityQueue with no root.
        '''
        self.heap: List[Node] = [None] #index 0 is filler, root is at index 1 (more readable indexes)
        self.root = None
    
    @classmethod
    def PriorityQueue(cls, root):
        '''
        Initialize a PriorityQueue with the root.
        '''
        new = cls.__new__(cls)
        super(PriorityQueue, new).__init__()
        new.heap = [None] #nothing at index 0; root at index 1
        new.root = root
        new.heap.append(root)
        return new

    def swap(self, node1, node2):
        '''
        Swap two nodes in the heap.
        '''
        self.heap[node1], self.heap[node2] = self.heap[node2], self.heap[node1]

    def up_heap(self, node_ind):
        '''
        Restore heap property by comparing nodes with their parent nodes and swapping upwards.
        '''
        parent_ind = floor(node_ind/2)
        parent = self.heap[parent_ind]
        node = self.heap[node_ind]
        if parent is not None and parent > node: #swap upwards if parent is greater
            self.swap(node_ind, parent_ind)
            self.up_heap(parent_ind)
        
    def down_heap(self, node_ind: int):
        '''
        Restore heap property by comparing nodes with their child nodes and swapping downwards.
        '''
        left_ind = 2*node_ind
        right_ind = 2*node_ind+1
        try:
            left = self.heap[left_ind]
        except IndexError: #could go OOB
            left = None 
        try:
            right = self.heap[right_ind]
        except IndexError:
            right = None
        cur_node = self.heap[node_ind]

        if (left is not None and left < cur_node) or (right is not None and right < cur_node): #needs to be swapped downwards if children are smaller
            if left is None and right is not None:
                smaller = right_ind
            elif right is None and left is not None:
                smaller = left_ind
            else:
                smaller = left_ind if left < right else right_ind

            self.swap(node_ind, smaller)
            self.down_heap(smaller)

    def insert(self, node: Node):
        '''
        Insert a node into the heap.
        '''
        if not self.root: #set as root if no root
            self.heap.append(node)
            self.root = self.heap[1]
            return
        self.heap.append(node)
        self.up_heap(len(self.heap)-1) # min-heapify
    
    def delete(self, node: Node):
        '''
        Remove a node from the heap.
        '''
        if self.length() == 1:
            self.heap.pop()
            return

        node_ind = self.heap.index(node)
        last_node_ind = len(self.heap)-1
        up_heapify = True if self.heap[last_node_ind] < node else False #up_heap needed if the swapped element is less than the deleted element, down_heap if the swapped element is greater than the deleted element
        
        self.swap(node_ind, last_node_ind) #swap node-to-delete with last node in heap
        self.heap.pop()

        if up_heapify:
            self.up_heap(node_ind)
        else:
            self.down_heap(node_ind)
    
    def extract_min(self) -> Node:
        '''
        Remove and return the minimum node (the root).
        '''
        minimum = self.heap.pop(1) #remove root
        if self.length() == 0:
            return minimum

        self.heap.insert(1, self.heap.pop()) #replace root with last element
        self.down_heap(1)  #min-heapify 
        return minimum
    
    def get_min(self) -> Node:
        '''
        Return the minimum node (root), but do not remove it.
        '''
        return self.heap[1]
    
    def decrease_key_dijk(self, node: Node, new_dist):
        '''
        Decrease the value of a particular node to { new_dist }.

        This will change Node.dist (dijkstra)
        '''
        node_ind = self.heap.index(node)
        self.heap[node_ind].set_dist(new_dist) #replace node's distance
        self.up_heap(node_ind) #up-heapify since value has been decreased
    
    def decrease_key_A(self, node: Node, new_score):
        '''
        Decrease the value of a particular node to { new_score }.

        This will change Node.f_score (A*)
        '''
        node_ind = self.heap.index(node)
        self.heap[node_ind].set_fScore(new_score) #replace node's f_score
        self.up_heap(node_ind) #up-heapify since value has been decreased

    def get_heap(self):
        '''
        Returns the heap.
        '''
        return self.heap[1:]
    
    def length(self):
        '''
        The length of the heap.
        '''
        return len(self.heap[1:])

    def visualize_heap(self):
        '''
        Prints an in-order traversal of the heap.
        '''
        ret = ''
        for i in self.heap[1:]:
            ret += f"{i} "

        return ret
        
    def __str__(self):
        return self.visualize_heap()
