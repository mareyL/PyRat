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
import numpy
from AIs import Dijkstra


###############################
movements = list()


def create_vertices_meta_graph(piece_of_cheese, player_location):
    return([player_location]+piece_of_cheese)

def create_edge_weight_maze_graph(maze_graph,vertices):
    adjacency_matrix={}
    for vertex in vertices: # for each vertex in vertices:
        source_vertex=vertex#     considere this vertex as source vertex
        explored_vertices,parent_dict,distances=Dijkstra.Dijkstra(maze_graph,source_vertex)#     use this source vertex and maze_graph to browse the graph with dijkstra algorithm
        adjacency_matrix[source_vertex]=distances#     use adjacency_matrix to store distances between source vertex and each vertex in the graph.
    return (adjacency_matrix)


def auxbf(current_walk,best_walk,adjacency_matrix,vertices,current_distance,best_distance):
    if (len(current_walk)>len(vertices)):# First we test if the current walk have gone through all vertices
        if (current_distance<best_distance): # if that is the case, we compare the current distance to the best distance
            best_distance=current_distance
            best_walk=current_walk  # and in the case it is better we update the best distance and the best walk 
    else:
        for vertex in vertices:# if the current_walk is not finished, for each possible vertex not explored,
            if vertex not in current_walk:
                best_walk_temp, best_distance_temp = auxbf(current_walk+[vertex],best_walk,adjacency_matrix,vertices,current_distance + adjacency_matrix[current_walk[-1]][vertex],best_distance) # we add it and call ourself recursively   
                if best_distance_temp < best_distance:
                    best_distance = best_distance_temp
                    best_walk = best_walk_temp
    return best_walk,best_distance

def bruteforceTSP(maze_graph,pieces_of_cheese,player_location):
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
    list_of_movement=list() #initialisation de la liste des mouvements
    best_walk, best_distance =bruteforceTSP(maze_graph,vertices,initial_vertex) # on retrouve le meilleur chemin et la meilleure distance à l'aide de la bruteforce
    for i in range(0,len(best_walk)-1): #construction de la liste de mouvements
        list_of_movement=list_of_movement+Dijkstra.A_to_B(maze_graph,best_walk[i],best_walk[i+1])
    return list_of_movement

def density(maze_graph,pieces_of_cheese):
    par_distance=10 #fixer un paramètre de distance pour délimiter les zones
    list_of_cheese=pieces_of_cheese[:] # copier la liste de fromages pour pouvoir la manipuler   
    list_of_groups=[] #Initialisation de la liste des groupes de fromages suivant le paramètre distance
    i=0 #compteur   
    for vertex1 in pieces_of_cheese:
        if vertex1 in list_of_cheese: #on considère un fromage A
            _,_,distances=Dijkstra.Dijkstra(maze_graph,vertex1)
            list_of_groups.append([])
            for vertex2 in pieces_of_cheese:
                if (distances[vertex2]<par_distance and vertex2 in list_of_cheese): # pour chaque fromage B on vérifie s'il est dans le cercle de rayon (paramètre distance )  et de centre fromage A
                    list_of_groups[i].append(vertex2) # on l'ajoute au i éme regroupement de fromages  
                    list_of_cheese.remove(vertex2) # on l'enlève pourqu'il ne figure pas une deuxième fois
            i=i+1
    return(list_of_groups)
                
def chemin(maze_graph,player_location,pieces_of_cheese):
    list_of_movements = [] #intitialisation de la liste de mouvements
    list_of_groups = density(maze_graph,pieces_of_cheese)
    sortedList_of_groups = [] 
    d,pos = 0,0   
    for i in range(len(list_of_groups)): #le but de cette boucle est de trier la liste_of_groups suivant un ordre décroissant de la taille des regroupements de fromages 
        pos=i
        if(len(list_of_groups[i])>d):
            d = len(list_of_groups[i])
        for j in range(i):
            if(len(list_of_groups[i])>len(sortedList_of_groups[j])):
                pos = j
                break
        sortedList_of_groups.insert(pos,list_of_groups[i])
    ######
    lonely_cells = [table[0] for table in sortedList_of_groups if len(table) == 1] #regrouper tous les regroupements de taille 1 dans une même liste 
    new_sortedList_of_groups = [table for table in sortedList_of_groups if not(len(table) == 1)]
    sortedList_of_groups = new_sortedList_of_groups
    ######
    bestGeneral_walk = []
    initial_vertex = player_location
    for table in sortedList_of_groups: #trouver la meilleur marche sur les regroupements de taille différente de 1 suivant l'algorithme "BruteForceTSP"
        best_walk,best_distance = bruteforceTSP(maze_graph,table,initial_vertex)
        initial_vertex = best_walk[-1]
        bestGeneral_walk += best_walk[1:]
    bestGeneral_walk = [player_location]+bestGeneral_walk
    ####
    if(len(lonely_cells)>6): #appliquer l'algorithme de "bruteForceTSP" sur la liste lonely_cells (d'un seul coup si sa taille est <= 6 ou sur deux coups sinon à cause du temps de calcul de bruteForceTSP
        bestGeneral_walk += bruteforceTSP(maze_graph,lonely_cells[0:len(lonely_cells)//2],bestGeneral_walk[-1])[0][1:]
        bestGeneral_walk += bruteforceTSP(maze_graph,lonely_cells[len(lonely_cells)//2:],bestGeneral_walk[-1])[0][1:]
    else:
        bestGeneral_walk += bruteforceTSP(maze_graph,lonely_cells,bestGeneral_walk[-1])[0][1:]
    ####    
    for i in range(len(bestGeneral_walk)-1): #determiner la liste des mouvements à partir de la meilleure marche
        list_of_movements+=(Dijkstra.A_to_B(maze_graph,bestGeneral_walk[i],bestGeneral_walk[i+1]))
    return(list_of_movements)

    
def FIFO_pop(FIFO_queue):
    return FIFO_queue.pop(0) 

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
    movements=chemin(maze_graph,playerLocation,piecesOfCheese)

    
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
    global movements
    return FIFO_pop(movements)
        
