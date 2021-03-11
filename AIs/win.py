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

def create_vertices_meta_graph(piece_of_cheese, player_location):
    return piece_of_cheese+[player_location]

def create_edge_weight_maze_graph(maze_graph,vertices):
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
    # First we test if the current walk have gone through all vertices
    if len(current_walk)>len(vertices):
        
        # if that is the case, we compare the current distance to the best distance
        if current_distance<best_distance:
            # and in the case it is better we update the best distance and the best walk
            best_distance=current_distance
            best_walk=current_walk
            
    # if the current_walk is not finished, for each possible vertex not explored,
    else:
        if current_distance<best_distance:# we add it and call ourself recursively
            for next_vertex in vertices:
                if not(next_vertex in current_walk):
                    walk,distance=auxbf(current_walk+[next_vertex],best_walk,adjacency_matrix,vertices,current_distance+adjacency_matrix[current_walk[-1]][next_vertex],best_distance)
                    
                    if distance<best_distance:
                        best_distance=distance
                        best_walk=walk
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
    list_of_movement=list()
    
    best_walk,_=bruteforceTSP(maze_graph,vertices,initial_vertex)
    
    for i in range(1,len(best_walk)):
        list_of_movement.append(A_to_B(maze_graph,best_walk[i-1],best_walk[i]))
    return sum(list_of_movement,[])

def FIFO_pop(FIFO_queue):
    return FIFO_queue.pop(0)

movements = list()

def choose_target(distances,pieces_of_cheese):
    distance = float('inf')
    next_target = None
    # for each vertex in pieces of cheese
    for vertex in pieces_of_cheese:
        #    compare its distance from player location with distance variable value.
        if distances[vertex]<distance:
            #    update distance varible with the smalest value
            distance=distances[vertex]
            #    keep the nearest vertex from player location
            next_target=vertex
    # returns the nearest vertex to be next target 
    
    return next_target


movements = list()

def movements_greedy_algorithm(maze_graph,pieces_of_cheese,player_location):
    
    # get distances using Dijkstra algorithm
    parent_dict,distances=Dijkstra(maze_graph,player_location)[1],Dijkstra(maze_graph,player_location)[2]
    # get next_target using choose_target function
    next_target=choose_target(distances,pieces_of_cheese)
    # use A_to_B function to get a list of movements that should be done to reach the nearest piece of cheese
    movements=A_to_B(maze_graph,player_location,next_target)
    # from player location
    return movements,next_target

def check_eat_cheese(player_location,opponent_location,player_score,opponent_score,pieces_of_cheese):
    if player_location in pieces_of_cheese and player_location == opponent_location:
        player_score+=0.5
        opponent_score+=0.5
        pieces_of_cheese.remove(player_location)
        # Add 0.5 to each player score
        # Remove the piece of cheese of the player location from the pieces_of_cheese list 
    else:
        if player_location in pieces_of_cheese:
            player_score+=1
            pieces_of_cheese.remove(player_location)
            # Add 1.0 to the player score
            # Remove the piece of cheese of the player location from the pieces_of_cheese list 
        if opponent_location in pieces_of_cheese:
            opponent_score+=1
            pieces_of_cheese.remove(opponent_location)
            # Add 1.0 to the opponent score
            # Remove the piece of cheese of the opponent location from the pieces_of_cheese list 
    return player_score,opponent_score

def target_choice(targets,pieces_of_cheese):
    for target in targets:
        if target in pieces_of_cheese:
            return target
    return None

def create_turn_target_function(targets):
    targets = targets.copy()

    def internal_turn_target(maze_graph, width,height, player1_location, player2_location, player1_score, 
            player2_score, pieces_of_cheese, time_allowed):
        target=A_to_B(maze_graph,player1_location,target_choice(targets,pieces_of_cheese))
        return target.pop(0)
    return internal_turn_target

def end_game(pieces_of_cheese,player1_score,player2_score,rounds,max_rounds = 1000):
    totalPieces = len(pieces_of_cheese) + player1_score + player2_score
    if rounds > max_rounds or player1_score > totalPieces / 2 or player2_score > totalPieces / 2 or len(pieces_of_cheese) == 0:
        return True
    else:
        return False

def simulate_move(
    maze_graph,width,height,player1_location,player2_location,
    player1_score,player2_score,pieces_of_cheese,
    turn_player1,turn_player2):    
    pieces_of_cheese = pieces_of_cheese.copy()
    # Get the decision of both players using the turn functions
    # Use the decisions to move the players using the utils.move function
    # Update the player1_location and player2_location variable after the move
    
    player1_decision=turn_player1(maze_graph,width,height,player1_location,player2_location, player1_score,player2_score,pieces_of_cheese,1)
    player2_decision=turn_player2(maze_graph,width,height,player2_location,player1_location, player2_score,player1_score,pieces_of_cheese,1)
    
    player1_location=utils.move(maze_graph,player1_location,player1_decision)
    player2_location=utils.move(maze_graph,player2_location,player2_decision)
    
    player1_score,player2_score = check_eat_cheese(
        player1_location,player2_location,player1_score,player2_score,pieces_of_cheese
    )
    return player1_location,player2_location,player1_score,player2_score,pieces_of_cheese

def simulate_game(maze_graph,width,height,player1_location,player2_location,
    player1_score,player2_score,pieces_of_cheese,
    turn_player1,turn_player2):
    pieces_of_cheese = pieces_of_cheese.copy()
    rounds = 0
    while not end_game(pieces_of_cheese,player1_score,player2_score,rounds):
        rounds += 1
        player1_location,player2_location,player1_score,player2_score,pieces_of_cheese=simulate_move(
    maze_graph,width,height,player1_location,player2_location,
    player1_score,player2_score,pieces_of_cheese,
    turn_player1,turn_player2)
        
        
    rounds += 1
    return player1_location,player2_location,player1_score,player2_score,pieces_of_cheese,rounds
    

import itertools

def full_combinatorial_game(maze_graph,width,height,pieces_of_cheese,player1_location,player2_location,turn_opponent):
    all_possible_permutations = list(itertools.permutations(pieces_of_cheese.copy()))
    best_order = None
    best_difference = -float("inf")
    best_rounds = float("inf")
    for order in all_possible_permutations:
        player1_score=0
        player2_score=0
        
        targets = list(order).copy()
        
        turn=create_turn_target_function(targets)
        
        new_player1_location,new_player2_location,new_player1_score,new_player2_score,new_pieces_of_cheese,rounds=simulate_game(
            maze_graph,width,height,player1_location,player2_location,
            player1_score,player2_score,pieces_of_cheese,
            turn,turn_opponent)
        
        difference=new_player1_score-new_player2_score
        
        if difference>best_difference or (difference==best_difference and rounds<best_rounds):                                         
            best_difference=difference
            best_order=targets
            best_rounds=rounds
        
    return best_order,best_difference,best_rounds
   

def turn_opponent(maze_graph, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global movements
    # if movements is empty, get list of movements that have to be performed to follow a shortest
    if movements==[]:
        # path from player location to reach next target 
        movements=movements_greedy_algorithm(maze_graph,piecesOfCheese,playerLocation)[0]
        #  else return the next movement we should perform to reach next target  
    return movements.pop(0)

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

def preprocessing():
    return()


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

targets=full_combinatorial_game(maze_graph,mazeWidth,mazeHeight,piecesOfCheese,playerLocation,opponentLocation,turn_opponent)[0]

turn=create_turn_target_function(targets)

