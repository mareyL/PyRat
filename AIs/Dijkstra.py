# Template file to create an AI for the game PyRat
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

import heapq 
import numpy

###############################
# Please put your global variables here

k=-1

def is_explored(explored_vertices,vertex):
    return vertex in explored_vertices

def add_to_explored_vertices(explored_vertices,vertex):
    explored_vertices.append(vertex)

def Dijkstra(maze_graph,initial_vertex):
    # Variable storing the exploredled vertices vertexes not to go there again
    explored_vertices = list()
    
    # Stack of vertexes
    heap = list()
    
    #Parent dictionary
    parent_dict = dict()
    # Distances dictionary
    distances = dict()
    
    # First call
    initial_vertex = (initial_vertex, 0, initial_vertex)    #vertex to visit, distance from origin, parent
    heapq.heappush(heap,initial_vertex)
    while len(heap) > 0:
        triplet=heapq.heappop(heap)                          # get the triplet (vertex, distance, parent) with the smallest distance from heap list using heap_pop function.
        if not(is_explored(explored_vertices,triplet[0])):  # if the vertex of the triplet is not explored:
            neighbor_dict=maze_graph[triplet[0]]
            parent_dict[triplet[0]]=triplet[2]              #     map the vertex to its corresponding parent
            explored_vertices.append(triplet[0])            #     add vertex to explored vertices.
            distances[triplet[0]]=triplet[1]                #     set distance from inital_vertex to vertex
            for i,wi in neighbor_dict.items():              #     for each unexplored neighbor i of the vertex, connected through an edge of weight wi
                heapq.heappush(heap,(i,wi+triplet[1],triplet[0]))       #         add (i, distance + wi, vertex) to the heap
        
    return explored_vertices, parent_dict, distances

def A_to_B(maze_graph,initial_vertex,target_vertex):
    parent_dict=Dijkstra(maze_graph,initial_vertex)[1]# use the Dijkstra algorithm to generate parent_dictionary
    walk=create_walk_from_parents(parent_dict,initial_vertex,target_vertex)# use the parent_dictionary, the source vertex, and end vertex to generate a walk between these two points using the utils.create_walk_from_parents function.
    return walk_to_route(walk,initial_vertex)# return a list of movements using the utils.walk_to_route function.

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
    
