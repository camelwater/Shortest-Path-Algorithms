from Algorithm import Algorithm
from PriorityQueue import PriorityQueue
from Graph import Graph
from A_Star_Node import A_Node
from math import sqrt
import time
import cProfile
from utils import nudge, reconstruct_path
# import pygame

def H(cur: A_Node, dest: A_Node):
    '''
    heuristic function (distance from current node to the target node)
    '''
    D = 1

    if allow_diagonal_movements:
        D2 = sqrt(2)
        dx, dy = abs(cur.x - dest.x), abs(cur.y - dest.y)
        return D * max(dx, dy) + (D2 - D) * min(dx, dy)
        # return sqrt((cur.x - dest.x)**2 + (cur.y - dest.y)**2)

    return D * (abs(cur.x - dest.x) + abs(cur.y - dest.y))

def D(cur: A_Node, neighbor: A_Node):
    '''
    edge weight between current node and neighbor (distance between the two nodes)
    '''
    D = 1

    if allow_diagonal_movements: #octile distance for 8-direction movements; Manhattan distance for 4-direction
        D2 = sqrt(2)
        dx, dy = abs(cur.x - neighbor.x), abs(cur.y - neighbor.y)
        return D * max(dx, dy) + (D2 - D) * min(dx, dy)
        # return sqrt((cur.x - dest.x)**2 + (cur.y - dest.y)**2)

    return D * (abs(cur.x - neighbor.x) + abs(cur.y - neighbor.y)) + nudge(cur, neighbor)


def A_star(source: A_Node, destination: A_Node):
    '''
    Find the shortest path between the source and destination nodes using the A* search algorithm.
    '''
    # prev = {}
    open_set = PriorityQueue.with_root(source) #min-heap priority queue
    
    source.set_gScore(0)
    source.set_fScore(H(source, destination))

    while open_set.length()>0:
        current = open_set.extract_min()

        if current == destination:
            print(f"Found the shortest path from node {source} to node {destination} - {current.f_score:.2f} nodes long.\n")
            # reconstruct_path(source, current)
            return 
        
        for neighbor in current.get_neighbors():
            eval_gScore = current.g_score + D(current, neighbor)
            if eval_gScore < neighbor.g_score:
                neighbor.set_gScore(eval_gScore)
                neighbor.prev = current
                # prev[neighbor] = current
                neighbor.set_fScore(eval_gScore + H(neighbor, destination))
                if not open_set.contains(neighbor):
                    open_set.insert(neighbor)
                
    print("No path could be found.")

def main():
    graph = Graph(1000, 1000, algo=Algorithm.A_STAR, allow_diagonal=allow_diagonal_movements)
    print("Finished building graph.")
    start = graph.get()[269][378]
    end = graph.get()[877][721]

    start_time = time.time()
    # prof = cProfile.Profile()
    # prof.enable()
    A_star(start, end)
    # prof.disable()
    # prof.print_stats()
    print(f"found in: {time.time()-start_time} sec")

if __name__ == "__main__":
    allow_diagonal_movements = False
    main()