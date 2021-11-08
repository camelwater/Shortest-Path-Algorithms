from math import floor
from typing import List, Dict
from Node import Node
from A_Star_Node import A_Node
from DijkNode import Dijk_Node


class PriorityQueue:
    '''
    min-heap priority queue.
    '''

    def __init__(self):
        '''
        Initialize PriorityQueue with no root.
        '''
        self.heap: List[Node] = [] #root is at index 0
        # self.rank = {} #used to break ties (more recent insertions are treated as smaller)
        self.insertion_num = -1
        self.index: Dict[Node, int] = {} #map nodes to their current indices in the heap
    
    @classmethod
    def with_root(cls, root: Node) -> 'PriorityQueue':
        '''
        Initialize a PriorityQueue with the root.
        '''
        pq = cls.__new__(cls)
        pq.__init__()
        pq.insert(root)
        return pq

    def swap(self, node1, node2):
        '''
        Swap two elements in the heap.
        '''
        self.heap[node1], self.heap[node2] = self.heap[node2], self.heap[node1]

    def up_heap(self, node_ind):
        '''
        Restore heap property by comparing elements with their parents and sifting upwards.
        '''
        node = self.heap[node_ind] # node being sifted up
        parent_ind = floor((node_ind-1)/2)

        while parent_ind > 0 and self.heap[parent_ind] > node: #sift up if parent is greater
            self.heap[node_ind] = self.heap[parent_ind] #parent being brought down
            self.index[self.heap[node_ind]] = node_ind
            node_ind = parent_ind
            parent_ind = floor((node_ind-1)/2)
        
        self.heap[node_ind] = node # node being sifted up placed at correct index
        self.index[self.heap[node_ind]] = node_ind

    def up_heap_rec(self, node_ind):
        parent_ind = floor((node_ind-1)/2)
        parent = self.heap[parent_ind]
        node = self.heap[node_ind]
        while parent is not None and parent > node: #swap upwards if parent is greater
            self.swap(node_ind, parent_ind)
            self.up_heap_rec(parent_ind)
        
    def down_heap(self, node_ind):
        '''
        Restore heap property by comparing elements with their children and sifting down.
        '''
        node = self.heap[node_ind] # node to be sifted down
        child_ind = 2*node_ind + 1 # left child

        while child_ind < len(self.heap): #children exist
            other_child_ind = child_ind + 1
            if other_child_ind < len(self.heap) and self.heap[other_child_ind] < self.heap[child_ind]: #switch to right child if it is smaller than left child
                child_ind = other_child_ind
            if not node > self.heap[child_ind]: #no need to keep sifting; children are not smaller
                break

            self.heap[node_ind] = self.heap[child_ind] #child brought up
            self.index[self.heap[node_ind]] = node_ind
            node_ind = child_ind # update node and child index
            child_ind = 2*node_ind + 1
        
        self.heap[node_ind] = node #put node to be sifted in place
        self.index[self.heap[node_ind]] = node_ind
    

    def insert(self, node: Node):
        '''
        Insert an element into the heap.
        '''
        
        node.inserted = self.insertion_num
        self.insertion_num-=1
        self.heap.append(node)
        
        if len(self.heap)==1: 
            self.index[node] = len(self.heap)-1
            return

        self.up_heap(len(self.heap)-1) # min-heapify
    
    def delete(self, node: Node):
        '''
        Remove an element from the heap.
        '''

        try:
            node_ind = self.index[node]
        except KeyError:
            raise KeyError("Cannot remove that node: node is not present in heap.")
        self.index.pop(node)

        if len(self.heap)==1:
            self.heap.pop(node_ind)
            return 

        last_node_ind = len(self.heap)-1
        up_heapify = True if self.heap[last_node_ind] < node else False #up_heap needed if the swapped element is less than the deleted element; down_heap if the swapped element is greater than the deleted element
        
        self.heap[node_ind] = self.heap.pop(last_node_ind) #replace deleted element with last element

        if up_heapify:
            self.up_heap(node_ind)
        else:
            self.down_heap(node_ind)
    
    def extract_min(self) -> Node:
        '''
        Remove and return the minimum element (the root).
        '''
        minimum = self.heap[0]
        self.index.pop(minimum)

        if len(self.heap) == 1:
            self.heap.pop()
            return minimum

        self.heap[0] = self.heap.pop() #replace root with last element
        self.down_heap(0) #min-heapify now that root could be too large 
        return minimum
    
    def get_min(self) -> Node:
        '''
        Return the minimum element (root), but do not remove it.
        '''
        return self.heap[0]
    
    def decrease_key_dijk(self, node: Dijk_Node, new_dist):
        '''
        Decrease the value (distance) of a particular Dijkstra Node to { new_dist }.

        This will change Dijk_Node.dist (dijkstra)
        '''
        node_ind = self.index[node]
        self.heap[node_ind].set_dist(new_dist) #replace node's distance
        self.up_heap(node_ind) #up-heapify since value has been decreased
    
    def decrease_key_A(self, node: A_Node, new_score):
        '''
        Decrease the value (f_score) of a particular A* Node to { new_score }.

        This will change A_Node.f_score (A*)
        '''
        node_ind = self.index[node]
        self.heap[node_ind].set_fScore(new_score) #replace node's f_score
        self.up_heap(node_ind) #up-heapify since value has been decreased

    def get_heap(self):
        '''
        Returns the heap.
        '''
        return self.heap
    
    def contains(self, node):
        '''
        Check whether an element is in the heap.
        '''
        return node in self.index
    
    def length(self):
        '''
        The length of the heap.
        '''
        return len(self.heap)
    
    def empty(self):
        return len(self.heap) == 0
    
    def clear(self):
        '''
        Empty the heap.
        '''
        self.heap = []

    def visualize_heap(self):
        '''
        Prints an in-order traversal of the heap.
        '''
        ret = ''
        for i in self.heap:
            ret += f"{i} "

        return ret

    def __str__(self):
        # return self.visualize_heap()
        return str(self.heap)


# if __name__ == "__main__":
#     node1 = A_Node(1, 1, 1)
#     node1.f_score = 1.1
#     pq = PriorityQueue.with_root(node1)
    
#     node2 = A_Node(2,2,2)
#     node2.f_score = 1.1
#     node3 = A_Node(3,3,3)
#     node4 = A_Node(4,4,4)
#     node3.f_score = 1.1
#     node4.f_score = 1.1
#     pq.insert(node2)
#     pq.insert(node3)
#     # pq.insert(node4)

#     pq.extract_min()
#     print(pq)