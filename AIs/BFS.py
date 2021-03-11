# Template file to ate an AI for the game PyRat
# http://formations.telecom-bretagne.eu/pyrat

###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

###############################
# Please put your imports here


###############################
# Please put your global variables here
k=-1
import numpy


moves=[]
###############################
# Preprocessing function
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int,int)
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is not expected to return anything
def FIFO_push(LIFO_list,element):
    LIFO_list.append(element)

def FIFO_pop(LIFO_list):
    return LIFO_list.pop(0)
    

def add_to_explored_vertices(explored_vertices,vertex):
    explored_vertices.append(vertex)

def is_explored(explored_vertices,vertex):
    return vertex in explored_vertices

def BFS(maze_graph, initial_vertex) :
    
    # explored vertices list
    explored_vertices = list()
    
    #FIFO stack
    queuing_structure = list()
    
    #Parent Dictionary
    parent_dict = dict()
        
    add_to_explored_vertices(explored_vertices,initial_vertex)#   explored_vertices = {start_vertex}

    FIFO_push(queuing_structure,initial_vertex) # push the initial vertex to the queuing_structure
    
    while len(queuing_structure) > 0: #   while queuing_structure is not empty:
        current_vertex=FIFO_pop(queuing_structure)
        
        neighbors_costs=maze_graph[current_vertex]
        
        for neighbor,cost in neighbors_costs.items():
            
            if not (is_explored(explored_vertices,neighbor)):
                
                add_to_explored_vertices(explored_vertices,neighbor)
                
                FIFO_push(queuing_structure,neighbor)
                
                parent_dict[neighbor]=current_vertex
       
    return explored_vertices,parent_dict  

def create_walk_from_parents(parent_dict,initial_vertex,target_vertex):
    s=target_vertex
    l=[]
    while s!=initial_vertex:
        for child in parent_dict.keys():
            if child==s:
                l.append(child)
                s=parent_dict[child]
    l.reverse()
    return(l)


def get_direction(initial_position,target_position):
    difference = tuple(numpy.subtract(target_position, initial_position))
    if difference==(1,0):
        return(MOVE_RIGHT)
    elif difference==(-1,0):
        return(MOVE_LEFT)
    elif difference==(0,1):
        return(MOVE_UP)
    elif difference==(0,-1):
        return(MOVE_DOWN)

def walk_to_route(walk,initial_vertex):
    l=[]
    l.append(get_direction(initial_vertex,walk[0]))
    for i in range (0,len(walk)-1):
        l.append(get_direction(walk[i],walk[i+1]))
    return(l)

def A_to_B(maze_graph,initial_vertex,target_vertex):
    explored_vertices,parent_dict=BFS(maze_graph, initial_vertex) 
    walk=create_walk_from_parents(parent_dict,initial_vertex,target_vertex)
    return(walk_to_route(walk,initial_vertex))
    

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
	global route
	route=A_to_B(mazeMap,playerLocation,piecesOfCheese[0])
	pass

    
###############################
# Turn function
# The turn function is called each time the game is waiting
# for the player to make a decision (a move).
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int, int)
# playerScore : float
# opponentScore : float
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is expected to return a move
def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
	global k
	if k<len(route)-1:
		k=k+1
		return(route[k])
