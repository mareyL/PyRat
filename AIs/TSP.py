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
    """
    Utilise l'algorithme de Dijkstra pour trouver le chemin le plus rapide entre deux noeuds.
    Prend en entrée le graph et le neoud initiale et renvoi une liste des noeuds explorés, un dictionnaire associant à chaque noeud son parent et un dictionnaire associant à       
    chaque noeud sa distance à l'origine.
    
    """
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
    """
    Prend en entrée le graph, et les deux noeuds à relier et renvoi une suite de direction pour s'y rendre.
    """
    parent_dict=Dijkstra(maze_graph,initial_vertex)[1]# use the Dijkstra algorithm to generate parent_dictionary
    walk=create_walk_from_parents(parent_dict,initial_vertex,target_vertex)# use the parent_dictionary, the source vertex, and end vertex to generate a walk between these two points using the utils.create_walk_from_parents function.
    return walk_to_route(walk,initial_vertex)# return a list of movements using the utils.walk_to_route function.

def create_walk_from_parents(parent_dict,initial_vertex,target_vertex):
    """
    Créer un chemin à partir du dictionnaire associant à chaque noeud son parent.
    """
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
    """
    Donne la direction dans laquelle il faut aller pour se déplacer d'un noeud à un autre noeud adjacent
    """
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
    """
    Créer une liste de direction à partir d'une liste de vertex adjacents.
    """
    l=[]
    l.append(get_direction(initial_vertex,walk[0]))
    for i in range (0,len(walk)-1):
        l.append(get_direction(walk[i],walk[i+1]))
    return(l)

def create_vertices_meta_graph(piece_of_cheese, player_location):
    """
    Renvoi le metagraph contenant la position du joueur et des fromages.
    """
    return piece_of_cheese+[player_location]

def create_edge_weight_maze_graph(maze_graph,vertices):
    """
    Renvoi un dictionnaire associant à chaque noeud les autres noeuds et la distance qui les sépare.
    """
    adjacency_matrix={}
    # for each vertex in vertices:
    #     considere this vertex as source vertex
    #     use this source vertex and maze_graph to browse the graph with dijkstra algorithm
    #     use adjacency_matrix to store distances between source vertex and each vertex in the graph.
    
    for initial_vertex in vertices:
        distances=Dijkstra(maze_graph,initial_vertex)[2]
        adjacency_matrix[initial_vertex] = {}
        for vertex in vertices:
            if vertex!=initial_vertex:
                adjacency_matrix[initial_vertex][vertex] = distances[vertex]
    return adjacency_matrix  

def auxbf(current_walk,best_walk,adjacency_matrix,vertices,current_distance,best_distance):
    """
    Fonction auxiliaire de bruteforceTSP récursive, renvoyant le chemin passant par tous les fromages avec une distance minimale.
    """
    # First we test if the current walk have gone through all vertices
    if len(current_walk)>len(vertices):
        
        # if that is the case, we compare the current distance to the best distance
        if current_distance<best_distance:
            # and in the case it is better we update the best distance and the best walk
            best_distance=current_distance
            best_walk=current_walk
            
    # if the current_walk is not finished, for each possible vertex not explored,
    else:
        # we add it and call ourself recursively
        for next_vertex in vertices:
            if not(next_vertex in current_walk):
                walk,distance=auxbf(current_walk+[next_vertex],best_walk,adjacency_matrix,vertices,current_distance+adjacency_matrix[current_walk[-1]][next_vertex],best_distance)
                
                if distance<best_distance:
                    best_distance=distance
                    best_walk=walk
    return best_walk,best_distance
                    
def bruteforceTSP(maze_graph,pieces_of_cheese,player_location):
    """
    Fait appel à auxbf
    """
    # first we compute the vertices of the meta_graph:
    vertices=create_vertices_meta_graph(pieces_of_cheese, player_location)
    
    # then we create the adjacency matrix of the meta graph
    adjacency_matrix = create_edge_weight_maze_graph(maze_graph,vertices)
    
    # now we can start defining our variables
    # current_distance is the length of the walk for the current exploration branch
    current_distance = 0
    # current_walk is a container for the current exploration branch
    current_walk = [player_location]
    # best_distance is an indicator of the shortest walk found so far
    best_distance = float('inf')
    # best_walk is a container for the corresponding walk
    best_walk = []
    
    # we start the exploration:
    best_walk, best_distance = auxbf(current_walk,best_walk,adjacency_matrix,pieces_of_cheese,current_distance,best_distance)
    return best_walk, best_distance

def A_to_all(maze_graph,initial_vertex,vertices):
    """
    Utilise bruteforceTSP pour construire une suite de directions à suivre pour prendre tous les fromages
    """
    list_of_movement=list()
    
    best_walk,_=bruteforceTSP(maze_graph,vertices,initial_vertex)
    
    for i in range(1,len(best_walk)):
        list_of_movement.append(A_to_B(maze_graph,best_walk[i-1],best_walk[i]))
    return sum(list_of_movement,[])

def FIFO_pop(FIFO_queue):
    return FIFO_queue.pop(0)

movements = list()


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

def preprocessing(maze_graph, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global movements
    # this function computes the list of movements from the previous exercise
    # and store them in the variable movements
    movements = A_to_all(maze_graph,playerLocation,piecesOfCheese)
    


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

def turn(maze_graph, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):    
    if movements!=[]:
        # this function returns the first movement in the variable movements
        # and removes it
        return FIFO_pop(movements) 
