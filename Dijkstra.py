from Algorithm import Algorithm
from dijkNode import Dijk_Node
from PriorityQueue import PriorityQueue
from Graph import Graph
import time


def L(cur: Dijk_Node, neighbor: Dijk_Node):
    '''
    return length of edge between two nodes
    (1 here again lmao)
    '''
    return 1

def reconstruct_path(source: Dijk_Node, dest: Dijk_Node):
    '''
    Prints out shortest path between source and destination nodes.
    '''
    path = []
    node = dest
    if not node.get_prev() and node != source: return "Failed to reconstruct path."

    while node.get_prev():
        path.append(node)
        node = node.get_prev()
    
    path.append(source)
    printed_path = ""
    for n in path[::-1]:
        printed_path+=f"{n} -> "
    print(printed_path.rstrip(" -> "))

def dijkstra(source: Dijk_Node, target: Dijk_Node):
    '''
    Dijkstra's algorithm to find the shortest path between two nodes.
    '''
    pq = PriorityQueue()
    queue = pq.PriorityQueue(source)
    source.set_dist(0)

    while queue.length()>0:
        current = queue.extract_min()

        if current == target:
            print(f"Found shortest path from node {source} to node {target} - {current.dist} nodes long.\n")
            reconstruct_path(source, current)
            return

        for neighbor in current.get_neighbors():
            alt = current.dist + L(current, neighbor)
            if alt < neighbor.dist:
                neighbor.set_dist(alt)
                neighbor.prev = current
                if neighbor not in queue.get_heap():
                    queue.insert(neighbor)
    
    print("No path could be found.")

def main():
    graph = Graph(100, 100, Algorithm.DIJKSTRA)
    start = graph.get()[17][21]
    end = graph.get()[47][69]
    start_time = time.time()
    dijkstra(start, end)
    print("found in:", time.time()-start_time)

if __name__ == "__main__":
    main()