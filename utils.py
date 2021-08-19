from Node import Node

def nudge(cur: Node, neighbor: Node):
    '''
    Adds an extremely small cost to some nodes/paths in order to favor more "straight" paths towards the goal.

    In many cases, there are several possible paths that are all optimal, so this allows the path to look a bit better, in my opinion.
    '''
    nudge = 0
    if (cur.x + cur.y) % 2 == 0 and neighbor.x != cur.x: nudge = 1
    elif (cur.x + cur.y) %2 ==1 and neighbor.y != cur.y: nudge = 1
    return nudge*(10**-5)

def reconstruct_path(source: Node, dest: Node):
    '''
    Prints out the shortest path between the source and destination nodes.
    '''
    path = []
    node = dest
    if not node.get_prev() and node!=source: print("Failed to reconstruct path.")

    while node.get_prev():
        path.append(node)
        node = node.get_prev()
    
    path.append(source)
    printed_path = ""
    for n in path[::-1]:
        printed_path+=f"{n} -> "
    print(printed_path.rstrip(" -> "))

def reconstruct_path_map(prev, source: Node, dest: Node):
    '''
    Prints out the shortest path between the source and destination nodes.
    '''
    path = []
    node = prev[dest]
    if not node and node!=source: print("Failed to reconstruct path.")

    while node in prev:
        path.append(node)
        node = prev[node]
    
    path.append(source)
    printed_path = ""
    for n in path[::-1]:
        printed_path+=f"{n} -> "
    print(printed_path.rstrip(" -> "))