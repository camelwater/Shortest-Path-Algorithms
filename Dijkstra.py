from Algorithm import Algorithm
from DijkNode import Dijk_Node
from PriorityQueue import PriorityQueue
from Graph import Graph
import time
from math import sqrt
from utils import nudge, reconstruct_path


def L(cur: Dijk_Node, neighbor: Dijk_Node):
    '''
    return length of edge between two nodes
    '''
    D = 1

    if allow_diagonal_movements: #octile distance for 8-direction movements; Manhattan distance for 4-direction
        D2 = sqrt(2)
        dx, dy = abs(cur.x - neighbor.x), abs(cur.y - neighbor.y)
        return D * max(dx, dy) + (D2 - D) * min(dx, dy)
        # return sqrt((cur.x - dest.x)**2 + (cur.y - dest.y)**2)

    return D * (abs(cur.x - neighbor.x) + abs(cur.y - neighbor.y)) + nudge(cur, neighbor)

def dijkstra(source: Dijk_Node, target: Dijk_Node):
    '''
    Dijkstra's algorithm to find the shortest path between two nodes.
    '''
    queue = PriorityQueue.with_root(source)
    source.set_dist(0)

    while not queue.empty():
        current = queue.extract_min()

        if current == target:
            print(f"Found shortest path from node {source} to node {target} - {current.dist:.2f} nodes long.\n")
            # reconstruct_path(source, current)
            return

        for neighbor in current.get_neighbors():
            alt = current.dist + L(current, neighbor)
            if alt < neighbor.dist:
                neighbor.set_dist(alt)
                neighbor.prev = current
                if not queue.contains(neighbor):
                    queue.insert(neighbor)
    
    print("No path could be found.")

def main():
    graph = Graph(1000, 1000, Algorithm.DIJKSTRA, allow_diagonal=allow_diagonal_movements)
    graph.set_up_neighbors()
    print("Finished constructing graph.")
    start = graph.get()[231][600]
    end = graph.get()[745][667]
    start_time = time.time()
    dijkstra(start, end)
    print("found in:", time.time()-start_time)

if __name__ == "__main__":
    allow_diagonal_movements = False
    main()