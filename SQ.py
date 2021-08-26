from collections import deque

class Queue:
    '''
    unbounded FIFO queue
    '''
    def __init__(self):
        self.queue = deque()
    
    def enqueue(self, item):
        self.queue.append(item)
    
    def dequeue(self):
        return self.queue.popleft()
    
    def contains(self, item):
        return item in self.queue
    
    def empty(self):
        return len(self.queue) == 0
    def get(self):
        return self.queue

class Stack:
    def __init__(self):
        self.stack = list()
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        return self.stack.pop()
    def contains(self, item):
        return item in self.stack
    def empty(self):
        return len(self.stack)==0
    def peek(self):
        try:
            return self.stack[-1]
        except IndexError:
            return None
    def get(self):
        return self.stack

class Iterator:
    def __init__(self, iter: list):
        self.iterator = iter
        self._index = -1
    def next(self):
        self._index += 1
        return self.iterator[self._index]
    def hasNext(self):
        try:
            _ = self.iterator[self._index+1]
            return True
        except IndexError:
            return False
    def get(self):
        return self.iterator
