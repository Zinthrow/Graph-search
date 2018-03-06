# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph
import queue
## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    open_set = queue.Queue()
    closed_set = set()
    meta = dict()
    meta[start] = (None)
    open_set.put(start)
    while not open_set.empty():
        parent_state = open_set.get()
        if parent_state == goal:
            return construct_path(parent_state,meta) 
        for child_state in graph.get_connected_nodes(parent_state):
            if child_state in closed_set:
                continue
            if child_state not in list(open_set.queue):
                meta[child_state] = (parent_state)
                open_set.put(child_state)        
        closed_set.add(parent_state)
            
def construct_path(state, meta):
    action = state
    while True:
        row = meta[state]
        if type(row) is not type(None):
            state = row
            action = state + action  
        else:
            break
    return (action)
        
    
## Once you have completed the breadth-first search,
## this part should be very simple to complete.
'''
discovered = dict()
meta = dict()
closed_set = set()
def dfs(graph, v ,goal):
    global discovered
    global meta
    global closed_set
    if bool(meta) == False:
        meta[v] = (None)
    discovered[v] = True
    if v == goal:
        return construct_path(v,meta)
    for edge in graph.get_connected_nodes(v):
        if edge not in closed_set:
            continue
        if edge not in discovered:
            discovered[edge] = False
            meta[edge] = v
        if discovered[edge] != True:
            dfs(graph, edge, goal)
'''                
def dfs(graph,start, goal): # This is a non-recursive dfs
    open_set = queue.LifoQueue()
    closed_set = set()
    meta = dict()
    
    meta[start] = (None)
    open_set.put(start)
    
    while not open_set.empty():
        parent_state = open_set.get()
        if parent_state == goal:
            return construct_path(parent_state,meta) 
        for child_state in graph.get_connected_nodes(parent_state):
            if child_state in closed_set:
                continue
            if child_state not in list(open_set.queue):
                meta[child_state] = (parent_state)
                open_set.put(child_state)       
        closed_set.add(parent_state)
## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.

def hill_climbing(graph,start, goal):
    open_set = queue.LifoQueue()
    closed_set = set()
    meta = dict()
    meta[start] = (None)
    open_set.put(start)
    while not open_set.empty():
        parent_state = open_set.get()
        if parent_state == goal:
            return list(construct_path(parent_state,meta))
        list_heuristic = []
        list_edge = []
        for edge in graph.get_connected_nodes(parent_state):
            heuristic = graph.get_heuristic(edge,goal)
            if edge in closed_set:
                continue           
            else:#if edge not in list(open_set.queue):
                if edge in list(open_set.queue):
                    open_set.queue.remove(edge)
                list_heuristic.append(heuristic)
                list_edge.append(edge)       
        sorted_edges = [e for h, e in sorted(zip(list_heuristic,list_edge))]
        for edge in sorted_edges[::-1]:
            meta[edge] = (parent_state)
            open_set.put(edge)
        closed_set.add(parent_state)
        
                              



## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
        
def beam_search(graph, start, goal, beam_width):
    open_set = queue.Queue()
    closed_set = set()
    meta = dict()
    meta[start] = (None)
    open_set.put(start)
    while not open_set.empty():
        parent_state = open_set.get()
        if parent_state == goal:
            return list(construct_path(parent_state,meta))
        list_heuristic = []
        list_edge = []
        for edge in graph.get_connected_nodes(parent_state):
            heuristic = graph.get_heuristic(edge,goal)
            if edge in closed_set:
                continue
            else: #if edge not in list(open_set.queue):
                if edge in list(open_set.queue):
                    open_set.queue.remove(edge)
                list_heuristic.append(heuristic)
                list_edge.append(edge)
        sorted_edges = [e for h, e in sorted(zip(list_heuristic,list_edge))]
        for edge in sorted_edges[:-(beam_width+1):-1]:
            meta[edge] = (parent_state)
            open_set.put(edge)
        closed_set.add(parent_state)
        
        
    

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    path_length = 0
    if graph.is_valid_path(node_names):
        for ind,node in enumerate(node_names[:-1]):
            edge_length = graph.get_edge(node, node_names[ind+1]).length
            path_length += edge_length
    else:
        print ('invalid path')
    return path_length
            

def branch_and_bound(graph, start, goal):
    open_set = queue.Queue()
    closed_set =set()
    found_paths = set()
    meta = dict()
    meta[start] = (None)
    open_set.put(start)
    bpal= ("", float('inf')) #best path and length
    while not open_set.empty():
        parent_state = open_set.get()
        if parent_state == goal:
            found_paths.add(construct_path(parent_state,meta))
            bpal = best_path_and_length(graph,found_paths)
        for child_state in graph.get_connected_nodes(parent_state):
            if child_state in closed_set:
                continue
            elif child_state not in list(open_set.queue):
                meta[child_state] = (parent_state)
                open_set.put(child_state)  
            temp_path = construct_path(child_state, meta)
            if path_length(graph,temp_path) > bpal[1]:
                del meta[child_state]
                open_set.get()
        closed_set.add(parent_state)
    return list(bpal[0])
    
def best_path_and_length(graph, found_paths):
    best_path = ""
    shortest_value = float('inf')
    for path in found_paths:
        pathlength = path_length(graph, path)
        if pathlength < shortest_value:
            shortest_value = pathlength
            best_path = path
    return (best_path, shortest_value)
            
        

def a_star(graph, start, goal):
    open_set = queue.Queue()
    closed_set =set()
    found_paths = set()
    meta = dict()
    meta[start] = (None)
    open_set.put(start)
    bpal= ("", float('inf')) #best path and length
    while not open_set.empty():
        parent_state = open_set.get()
        list_heuristic = []
        list_states = []
        if parent_state == goal:
            found_paths.add(construct_path(parent_state,meta))
            bpal = best_path_and_length(graph,found_paths)
        for child_state in graph.get_connected_nodes(parent_state):
            heuristic = graph.get_heuristic(child_state,goal)
            if child_state not in list(open_set.queue):
                list_heuristic.append(heuristic)
                list_states.append(child_state)   
            
        sorted_edges = [e for h, e in sorted(zip(list_heuristic,list_states))]
        for edge in sorted_edges[::-1]:
            if edge in closed_set:
                continue
            elif edge not in list(open_set.queue):
                meta[edge] = (parent_state)
                open_set.put(edge)  
            temp_path = construct_path(edge, meta)
            if path_length(graph,temp_path) > bpal[1]:
                del meta[edge]
                open_set.get()
        closed_set.add(parent_state)
    return list(bpal[0])
    

        

'''
## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    raise NotImplementedError

def is_consistent(graph, goal):
    raise NotImplementedError

HOW_MANY_HOURS_THIS_PSET_TOOK = ''
WHAT_I_FOUND_INTERESTING = 'The small things you can do to ameliorate graph search time'
WHAT_I_FOUND_BORING = 'Converting python 2 to 3'
'''
