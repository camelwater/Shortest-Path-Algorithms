from typing import Iterator, List
from DijkNode import Dijk_Node
from Algorithm import Algorithm
from PriorityQueue import PriorityQueue
from Graph import Graph
from A_Star_Node import A_Node
from math import sqrt
from utils import nudge
import pygame
from pygame_widgets.button import Button
import pygame.draw
from operator import sub
from tkinter import messagebox
import tkinter as tk
from SQ import Queue

pygame.init()
pygame.display.init()
pygame.font.init()
SCR_WIDTH = 1400
SCR_HEIGHT = 750

SURFACE = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT)) #resizable?
pygame.display.set_caption("Shortest path visualization")
BOLD_FONT = pygame.font.SysFont('Segoe UI', 20, True)
BOLD_FONT_MASS = pygame.font.SysFont('Segoe UI', 50, True)
NORMAL_FONT = pygame.font.SysFont("Segoe UI", 20, False)
GRAPH = None

build_text = BOLD_FONT.render('BUILDING GRAPH...', True, (255, 255, 255))
finish_build_text = BOLD_FONT.render("Finished building graph.", True, (255,255,255))

a_star_button = None
dijk_button = None
bfs_button = None
start_button = None
visualize_button = None
build_button = None
diagonal_button = None
down_arrow = None
up_arrow = None
gen_rand_button = None

allow_diagonal_movements = False
random_obs = False
select_screen = False
setting_params = True
building_graph = False
algorithm = None
rows = 50
cols = 50

x_factor = SCR_WIDTH/(cols)
y_factor = SCR_HEIGHT/(rows)
size = min(x_factor, y_factor)*9/10
circle_rad = size*9/10 // 2

visualize = False
done = False

start = None
end = None


def H(cur: A_Node, dest: A_Node):
    '''
    heuristic function (distance from current node to the target node)
    '''
    D = 1

    if allow_diagonal_movements:
        D2 = sqrt(2)
        dx, dy = abs(cur.x - dest.x), abs(cur.y - dest.y)
        return D * max(dx, dy) + (D2 - D) * min(dx, dy)
        

    return D * (abs(cur.x - dest.x) + abs(cur.y - dest.y))
    # return sqrt((cur.x - dest.x)**2 + (cur.y - dest.y)**2)

def D(cur: A_Node, neighbor: A_Node):
    '''
    edge weight between current node and neighbor (distance between them)
    '''
    D = 1

    if allow_diagonal_movements: #octile distance for 8-direction movements; Manhattan distance for 4-direction
        D2 = sqrt(2)
        dx, dy = abs(cur.x - neighbor.x), abs(cur.y - neighbor.y)
        return D * max(dx, dy) + (D2 - D) * min(dx, dy)

    return D * (abs(cur.x - neighbor.x) + abs(cur.y - neighbor.y)) + nudge(cur, neighbor)

def reconstruct_path(source: A_Node, dest: A_Node, final = False):
    '''
    Displays the shortest path between the source and destination nodes.
    '''
    if not visualize:
        for row in GRAPH.get():
            for node in row:
                draw(node, is_sd=node in [source, dest])

    node = dest
    draw(node, (0, 255, 255) if final else (0, 0, 255))
    if not node.get_prev() and node!=source: print("Failed to reconstruct path.")

    while node.get_prev():
        node = node.get_prev()
        if node == source: break
        draw(node, (0,0,255), path=True)

    draw(source, (0, 255, 255) if final else (0, 0, 255))

    pygame.display.update()
    
def A_star(source: A_Node, destination: A_Node):
    '''
    Find the shortest path between the source and destination nodes using the A* search algorithm.
    '''
    # prev = {}
    open_set = PriorityQueue.with_root(source) #min-heap priority queue
    closed_set = []
    
    source.set_gScore(0)
    source.set_fScore(H(source, destination))
    
    while open_set.length()>0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if visualize:
            SURFACE.fill((255, 255, 255))
            for row in GRAPH.get():
                for node in row:
                    draw(node, is_sd=node in [source, destination])

        current = open_set.extract_min()
        closed_set.append(current)

        if current == destination:
            print(f"Found the shortest path from node {source} to node {destination} - {current.f_score:.2f} nodes long.\n")
            reconstruct_path(source, current, final=True)
            root = tk.Tk()
            root.withdraw()
            root.overrideredirect(1)
            messagebox.showinfo("!!!", f"Shortest path from node {source} to node {destination} :: {current.f_score:.2f} nodes long.")
            root.destroy()
            return True
        
        for neighbor in current.get_neighbors():
            eval_gScore = current.g_score + D(current, neighbor)
            if eval_gScore < neighbor.g_score:
                neighbor.set_gScore(eval_gScore)
                neighbor.prev = current
                # prev[neighbor] = current
                neighbor.set_fScore(eval_gScore + H(neighbor, destination))
                if not open_set.contains(neighbor):
                    open_set.insert(neighbor)
        
        if visualize:
            for node in open_set.get_heap():
                draw(node, (0, 255, 0))
            for node in closed_set:
                draw(node, (255, 0, 0))
            reconstruct_path(source, current)

            pygame.display.update()
                
    print("No path could be found.")
    not_found_text = BOLD_FONT_MASS.render("No path could be found.", True, (82, 27, 191))
    SURFACE.blit(not_found_text, ((SCR_WIDTH-not_found_text.get_width())/2, (SCR_HEIGHT-not_found_text.get_height())/2))
    return False

def dijkstra(source: Dijk_Node, target: Dijk_Node):
    open_set = PriorityQueue.with_root(source)
    visited = []

    source.set_dist(0)

    while open_set.length()>0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if visualize:
            SURFACE.fill((255, 255, 255))
            for row in GRAPH.get():
                for node in row:
                    draw(node, is_sd=node in [source, target])
        
        current = open_set.extract_min()
        visited.append(current)
        
        if current == target:
            print(f"Found the shortest path from node {source} to node {target} - {current.dist:.2f} nodes long.\n")
            reconstruct_path(source, current, final=True)
            root = tk.Tk()
            root.withdraw()
            root.overrideredirect(1)
            messagebox.showinfo("!!!", f"Shortest path from node {source} to node {target} :: {current.dist:.2f} nodes long.")
            root.destroy()

            return True

        for neighbor in current.get_neighbors():
            alt = current.dist + D(current, neighbor)
            if alt < neighbor.dist:
                neighbor.set_dist(alt)
                neighbor.prev = current
                if neighbor not in open_set.get_heap():
                    open_set.insert(neighbor)
        if visualize:
            for node in open_set.get_heap():
                draw(node, (0, 255, 0))
            for node in visited:
                draw(node, (255, 0, 0))
            reconstruct_path(source, current)

            pygame.display.update()
                
    print("No path could be found.")
    not_found_text = BOLD_FONT_MASS.render("No path could be found.", True, (82, 27, 191))
    SURFACE.blit(not_found_text, ((SCR_WIDTH-not_found_text.get_width())/2, (SCR_HEIGHT-not_found_text.get_height())/2))
    return False

def BFS(source, target):
    '''
    Find shortest path between two nodes with breadth-first search.
    '''
    queue = Queue()
    explored = set()
    explored.add(source)
    queue.enqueue(source)
    source.set_dist(0)

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if visualize:
            SURFACE.fill((255, 255, 255))
            for row in GRAPH.get():
                for node in row:
                    draw(node, is_sd=node in [source, target])

        current = queue.dequeue()

        if current == target:
            print(f"Found the shortest path from node {source} to node {target} - {current.dist:.2f} nodes long.\n")
            reconstruct_path(source, current, final=True)
            root = tk.Tk()
            root.withdraw()
            root.overrideredirect(1)
            messagebox.showinfo("!!!", f"Shortest path from node {source} to node {target} :: {current.dist:.2f} nodes long.")
            root.destroy()
            return True
        
        for neighbor in current.get_neighbors():
            if neighbor not in explored:
                neighbor.set_dist(current.dist + D(current, neighbor))
                neighbor.prev = current
                queue.enqueue(neighbor)
                explored.add(neighbor)
        
        if visualize:
            for node in explored:
                draw(node, (255, 0, 0))
            for node in queue.get():
                draw(node, (0, 255, 0))
            reconstruct_path(source, current)

            pygame.display.update()

    print("No path could be found.")
    not_found_text = BOLD_FONT_MASS.render("No path could be found.", True, (82, 27, 191))
    SURFACE.blit(not_found_text, ((SCR_WIDTH-not_found_text.get_width())/2, (SCR_HEIGHT-not_found_text.get_height())/2))
    return False


def clear_nodes():
    for row in GRAPH.get():
        for node in row:
            node.clear()

def create_graph():
    global GRAPH
    recalc_scale()
    GRAPH = Graph(rows, cols, algorithm, allow_diagonal=allow_diagonal_movements)

def recalc_scale():
    global x_factor, y_factor, circle_rad, size

    x_factor = SCR_WIDTH/cols
    y_factor = SCR_HEIGHT/rows
    size = min(x_factor, y_factor)*9/10
    circle_rad = size*9/10 // 2

def rebuild_graph():
    global GRAPH, start, end
    recalc_scale()
    temp_graph = Graph(rows, cols, algorithm, allow_diagonal=allow_diagonal_movements)

    if GRAPH.num_cols == temp_graph.num_cols and GRAPH.num_rows == temp_graph.num_rows:
        for r in range(len(GRAPH.get())):
            for c in range(len(GRAPH.get()[r])):
                temp_graph.get()[r][c].obstacle = GRAPH.get()[r][c].obstacle
                if GRAPH.get()[r][c] == start:
                    start = temp_graph.get()[r][c]
                if GRAPH.get()[r][c] == end:
                    end = temp_graph.get()[r][c]   
    else:
        start = end = None 
    GRAPH = temp_graph

def create_button(text, x, y, w, h, color=None):
    color = color or (150, 150, 150)
    button = Button(
        SURFACE, x, y, w, h,
        text=text, fontSize = min(int(w//(len(text)/(8/3))), int(w/7)), margin=50, 
        colour = color,
        hoverColour = tuple(map(sub, color, (25, 25, 25))),
        radius = 20
    )
    return button

def get_rect(button: Button) -> pygame.Rect:
    return pygame.Rect(button.getX(), button.getY(), button.getWidth(), button.getHeight())

def draw(node: A_Node, color = None, is_sd=False, path=False):
    '''
    draw a node.
    '''
    if node.is_obstacle():
        pygame.draw.rect(SURFACE, (255, 255, 0), (node.x*x_factor+x_factor/2-circle_rad, node.y*y_factor+y_factor/2-circle_rad, size, size))
    else:
        if color is None:
            color = (0, 255, 255) if is_sd else (0,0,0)
        # if path:
        #     pygame.draw.rect(SURFACE, color, (node.x*x_factor, node.y*y_factor, x_factor, y_factor), 2)
        #     pygame.draw.rect(SURFACE, color, (node.x*x_factor+x_factor/2-circle_rad, node.y*y_factor+y_factor/2-circle_rad, size, size))
        # else:
            # pygame.draw.rect(SURFACE, (255, 0, 0), (node.x*x_factor, node.y*y_factor, x_factor, y_factor), 1)
        radius = circle_rad*5/4 if path else circle_rad
        pygame.draw.circle(SURFACE, color, (node.x*x_factor+(x_factor/2), node.y*y_factor+(y_factor/2)), radius)

def set_obstacle(pos):
    '''
    sets a node as an obstacle.
    '''
    x, y = pos[0], pos[1]
    row, col = x // (SCR_WIDTH / GRAPH.num_cols), y // (SCR_HEIGHT / GRAPH.num_rows)
    try:
        node = GRAPH.get()[int(row)][int(col)]
    except IndexError:
        return

    if node.is_obstacle():
        node.obstacle = False
        return
    if node not in [start, end]:
        node.set_obstacle()

def set_start(pos):
    '''
    sets the source node.
    '''
    global start
    x, y = pos[0], pos[1]
    row, col = x // (SCR_WIDTH / GRAPH.num_cols), y // (SCR_HEIGHT / GRAPH.num_rows)
    
    try:
        select = GRAPH.get()[int(row)][int(col)]
    except IndexError: 
        return

    if select == start:
        start = None
        return
    if select != end and not select.is_obstacle():
        start = select
    
def set_end(pos):
    '''
    sets the target node.
    '''
    global end
    x, y = pos[0], pos[1]
    row, col = x // (SCR_WIDTH / GRAPH.num_cols), y // (SCR_HEIGHT / GRAPH.num_rows)
    
    try:
        select = GRAPH.get()[int(row)][int(col)]
    except IndexError:
        return

    if select == end:
        end = None
        return
    if select!=start and not select.is_obstacle():
        end = select

def draw_settings(events):
    '''
    draw settings buttons.
    '''
    global a_star_button, dijk_button, bfs_button, visualize_button, build_button, diagonal_button, up_arrow, down_arrow, gen_rand_button

    a_star_button = create_button("A*", x = (SCR_WIDTH-200)*1/4, y = (SCR_HEIGHT-100)/5, w = 200, h = 100, color = (79, 194, 131) if algorithm == Algorithm.A_STAR else None)
    a_star_button.listen(events)
    a_star_button.draw()
    dijk_button = create_button("Dijkstra's", x = (SCR_WIDTH-200)*3/4, y = (SCR_HEIGHT-100)/5, w = 200, h = 100, color = (79, 194, 131) if algorithm == Algorithm.DIJKSTRA else None)
    dijk_button.listen(events)
    dijk_button.draw()
    bfs_button = create_button("Breadth-first", x = (SCR_WIDTH-200)*2/4, y = (SCR_HEIGHT-100)/5, w = 200, h = 100, color = (79, 194, 131) if algorithm == Algorithm.BFS else None)
    bfs_button.listen(events)
    bfs_button.draw()
    
    size_text = BOLD_FONT_MASS.render(f"Size: {rows}x{cols}", True, (255, 255, 255))
    SURFACE.blit(size_text, ((SCR_WIDTH-size_text.get_width())/2, (SCR_HEIGHT-size_text.get_height())*3/7)) 

    up_arrow = pygame.draw.polygon(SURFACE, (0, 115, 150), (((SCR_WIDTH-size_text.get_width())/2+(2/3*size_text.get_width()+15/2), 
                                                                (SCR_HEIGHT-size_text.get_height())*3/7-(1/4*size_text.get_height())),
                                                            ((SCR_WIDTH-size_text.get_width())/2+(2/3*size_text.get_width()), 
                                                                (SCR_HEIGHT-size_text.get_height())*3/7-(1/4*size_text.get_height())+15),
                                                            ((SCR_WIDTH-size_text.get_width())/2+(2/3*size_text.get_width())+15, 
                                                                (SCR_HEIGHT-size_text.get_height())*3/7-(1/4*size_text.get_height())+15)))

    down_arrow = pygame.draw.polygon(SURFACE, (0, 115, 150), (((SCR_WIDTH-size_text.get_width())/2+(2/3*size_text.get_width()+15/2), 
                                                                (SCR_HEIGHT-size_text.get_height())*3/7+(5/4*size_text.get_height())+15),
                                                            ((SCR_WIDTH-size_text.get_width())/2+(2/3*size_text.get_width()), 
                                                                (SCR_HEIGHT-size_text.get_height())*3/7+(5/4*size_text.get_height())),
                                                            ((SCR_WIDTH-size_text.get_width())/2+(2/3*size_text.get_width())+15, 
                                                                (SCR_HEIGHT-size_text.get_height())*3/7+(5/4*size_text.get_height()))))

    visualize_button = create_button(f"Visualize: {visualize}", x = (SCR_WIDTH-125)*1/3, y = (SCR_HEIGHT-75)*2/3, w = 125, h = 75)
    visualize_button.listen(events)
    visualize_button.draw()

    diagonal_button = create_button(f"Diagonals: {allow_diagonal_movements}", x = (SCR_WIDTH-125)*2/3, y = (SCR_HEIGHT-75)*2/3, w = 125, h = 75)
    diagonal_button.listen(events)
    diagonal_button.draw()

    gen_rand_button = create_button(f"Random obstacles: {random_obs}", x = (SCR_WIDTH-250)*1/2, y = (SCR_HEIGHT-75)*2/3, w = 250, h = 75)
    gen_rand_button.listen(events)
    gen_rand_button.draw()

    if algorithm and rows is not None and cols is not None:
        build_button = create_button("Build Graph", x = (SCR_WIDTH-250)/2, y = (SCR_HEIGHT-100)*9/10    , w = 250, h = 100)
        build_button.listen(events)
        build_button.draw()

def settings_mouseHandler(pos):
    '''
    handle mouse events in the settings screen.
    '''
    global algorithm, visualize, building_graph, setting_params, allow_diagonal_movements, rows, cols, random_obs
    if get_rect(a_star_button).collidepoint(pos):
        algorithm = Algorithm.A_STAR

    elif get_rect(dijk_button).collidepoint(pos):
        algorithm = Algorithm.DIJKSTRA
    
    elif get_rect(bfs_button).collidepoint(pos):
        algorithm = Algorithm.BFS
    
    elif get_rect(visualize_button).collidepoint(pos):
        visualize = not visualize
    elif get_rect(diagonal_button).collidepoint(pos):
        allow_diagonal_movements = not allow_diagonal_movements
    elif get_rect(gen_rand_button).collidepoint(pos):
        random_obs = not random_obs
    
    elif up_arrow.collidepoint(pos):
        rows = cols = min(rows+25, 100)
    elif down_arrow.collidepoint(pos):
        rows = cols = max(rows-25, 25)

    elif algorithm and rows is not None and cols is not None and get_rect(build_button).collidepoint(pos):
        if not GRAPH: #not retrying
            create_graph()
        else: #retrying, so save the start+end nodes and obstacles
            rebuild_graph()
        
        if random_obs:
            GRAPH.generate_rand_obstacles([start, end])

        building_graph = True
        setting_params = False

def mouseHandler(events):
    global select_screen, start, end
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if select_screen and start and end:
                    select_screen = False
                    GRAPH.set_up_neighbors()
                    return
            elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                if select_screen:
                    start = None
                    end = None
                    create_graph()
                    return

        if event.type == pygame.MOUSEBUTTONDOWN: #clicked on some node
            if event.button == 1: #left click (set starting node)
                if select_screen:
                    set_start(pygame.mouse.get_pos())
                elif setting_params:
                    settings_mouseHandler(pygame.mouse.get_pos())
            elif event.button == 3: #right click (set ending node)
                if select_screen:
                    set_end(pygame.mouse.get_pos())
            elif event.button == 2: #middle click (set obstacles)
                if select_screen:
                    set_obstacle(pygame.mouse.get_pos())
        
            
def update_screen(events):
    global start_button, building_graph, select_screen, done
    mouseHandler(events)

    if setting_params: #choose settings
        SURFACE.fill((0, 0, 0)) 
        draw_settings(events)
    elif building_graph: #show building graph text
        SURFACE.fill((0,0,0))
        SURFACE.blit(build_text, ((SCR_WIDTH-build_text.get_width())/2, (SCR_HEIGHT-build_text.get_height())/2))
        building_graph = False
        select_screen = True
    elif select_screen:  #select start, end, and obstacle nodes
        SURFACE.fill((255, 255, 255)) 
        for row in GRAPH.get():
            for node in row:
                draw(node, is_sd = node in [start, end])
        
    else: #draw while the algorithm is running
        ALGO_MAP[algorithm](start, end)
        done = True

    pygame.display.update()

def main():
    global done, setting_params
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and done:
                    done = not done
                    setting_params = True
                    # clear_nodes()
                    break
        if not done:
            update_screen(events)    


if __name__ == "__main__":
    ALGO_MAP = {
        Algorithm.A_STAR: A_star,
        Algorithm.DIJKSTRA: dijkstra,
        Algorithm.BFS: BFS
        }
    main()
    