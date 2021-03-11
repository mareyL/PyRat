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
import time

###############################
# Please put your global variables here



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

def density(maze_graph,pieces_of_cheese):
    par_distance=10 #fixer un paramètre de distance pour délimiter les zones
    list_of_cheese=pieces_of_cheese[:] # copier la liste de fromages pour pouvoir la manipuler   
    list_of_groups=[] #Initialisation de la liste des groupes de fromages suivant le paramètre distance
    i=0 #compteur   
    for vertex1 in pieces_of_cheese:
        if vertex1 in list_of_cheese: #on considère un fromage A
            _,_,distances=Dijkstra(maze_graph,vertex1)
            list_of_groups.append([])
            for vertex2 in pieces_of_cheese:
                if (distances[vertex2]<par_distance and vertex2 in list_of_cheese): # pour chaque fromage B on vérifie s'il est dans le cercle de rayon (paramètre distance )  et de centre fromage A
                    list_of_groups[i].append(vertex2) # on l'ajoute au i éme regroupement de fromages  
                    list_of_cheese.remove(vertex2) # on l'enlève pourqu'il ne figure pas une deuxième fois
            i=i+1
    return(list_of_groups)

def chemin(maze_graph,pieces_of_cheese):
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
##    lonely_cells = [table[0] for table in sortedList_of_groups if len(table) == 1] #regrouper tous les regroupements de taille 1 dans une même liste 
##    new_sortedList_of_groups = [table for table in sortedList_of_groups if not(len(table) == 1)]
##    sortedList_of_groups = new_sortedList_of_groups
    return(sortedList_of_groups)

def mini(distances,g):
    mini=distances[g[0]]
    index=0
    for x in g:
        if distances[x]<mini:
            mini=distances[x]
            index=x
    return index

def adaptive_program(maze_graph,pieces_of_cheese,player_location,opponent_location):
    global cible,listOfTargets,movements,groupe_cible
    listOfTargets = list(set(listOfTargets)&set(pieces_of_cheese))#update our listOfTargets accordingly with the piecesOfCheese 
    if(opponent_location == cible)or(player_location == cible): #checks if the opponent has stolen our targeted piece of cheese or if we've made it to our targeted pieces of cheese
        cible = listOfTargets.pop(0)                        #and in both cases, we head to the next cheese in our list of targets 
        movements = A_to_B(maze_graph,player_location,cible)+A_to_all(maze_graph,cible,groupe_cible)

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


    
    
groupes = list()
listOfTargets = list()
cible = tuple()
movements = list()
groupe_cible=list()


def preprocessing(maze_graph, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global groupes,cible,listOfTargets,groupe_cible
    print("nombre de bout de fromage : ",len(piecesOfCheese))
    cible = playerLocation
    ##now we will construct our listOfTargets based on two criteria : we choose groups with max number of cheese and within those we start with minimum distance to the opponent 
    groupes = chemin(maze_graph,piecesOfCheese)
    # print("groupes de fromages : ",groupes,"   #######    ") ###
##    ### test
##    nombre = 0
##    for group in groupes:
##        nombre += len(group)
##    print(" nombre de bout de fromages dans les groupes : ",nombre)
##    ###
    _,_,Player_distances = Dijkstra(maze_graph,playerLocation)
    _,_,Opponent_distances = Dijkstra(maze_graph,opponentLocation)
    cheeseGroups = groupes.copy()
    while len(listOfTargets) < len(piecesOfCheese):
        size = len(cheeseGroups[0])
        sameSizeGroups = [cheeseGroups.pop(0)]
        while(cheeseGroups != [])and(len(cheeseGroups[0]) == size ):
            sameSizeGroups.append(cheeseGroups.pop(0))
        sortedSizeGroups = dict() #in this dict we will sort sameSizeGroups according to the distance of their first element to the oppponent 
        for group in sameSizeGroups:
            average=0
            for element in group:
                average += Opponent_distances[element]
            average = average / len(group)
            sortedSizeGroups[average] = group
            while(len(sortedSizeGroups) != 0):
                listOfTargets = listOfTargets + sortedSizeGroups.pop(min(list(sortedSizeGroups.keys())))
    ### end of listOfTargets's construction
    
    
    

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
    global groupes,listOfTargets,movements,cible,groupe_cible
    adaptive_program(maze_graph,piecesOfCheese,playerLocation,opponentLocation)
##    while k<len(groupes) :
##        if len(groupes[k]) != len( groupe[k+1]):
##            break
##    for h in range(k):
##        difference=-Opponent_distances[groupes[k][0]]+Player_distances[groupes[k][0]]: # si >= le groupe le plus près de player location sinon le groupe le plus près de opponent location        
##      groupes=chemin(maze_graph,playerLocation,piecesOfCheese)
##      if not(groupe_cible in groupes) or movements==[]:
##         if groupe_cible in groupes:
##             groupes.remove(groupe_cible)
##         if groupes!=[]:
##             k=0
##             _,_,Player_distances=Dijkstra(maze_graph,playerLocation)
##             _,_,Opponent_distances=Dijkstra(maze_graph,opponentLocation)
##             while len(groupes[k])==len(groupes[0]) and Opponent_distances[groupes[k][0]]>=Player_distances[groupes[k][0]]:
##                 k+=1
##             if k>=len(groupes):
##                 k=0
##             groupe_cible=groupes[k]
##             print(groupe_cible,k)
##             cible=mini(Player_distances,groupe_cible)
##             movements=A_to_B(maze_graph,playerLocation,cible)+A_to_all(maze_graph,cible,groupe_cible)
##         else:
##             movements=A_to_all(maze_graph,playerLocation,piecesOfCheese)
    return FIFO_pop(movements)

