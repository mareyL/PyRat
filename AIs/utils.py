from operator import itemgetter
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
        
def get_new_location(location, decision):
    if decision == MOVE_UP:
        return (location[0], location[1] + 1)
    elif decision == MOVE_DOWN:
        return (location[0], location[1] - 1)
    elif decision == MOVE_LEFT:
        return (location[0] - 1, location[1])
    elif decision == MOVE_RIGHT:
        return (location[0] + 1, location[1])
    else:
        return location

def move(maze,player_location,decision):
    new_location = get_new_location(player_location,decision)
    if new_location in maze[player_location]:
        return new_location
    else:
        return player_location

    
def get_position_above(original_position):
    """
    Given a position (x,y) returns the position above the original position, defined as (x,y+1)
    """
    (x,y) = original_position
    return (x,y+1)


def get_position_below(original_position):
    """
    Given a position (x,y) returns the position below the original position, defined as (x,y-1)
    """
    (x,y) = original_position
    return (x,y-1)

def get_position_right(original_position):
    """
    Given a position (x,y) returns the position to the right of the original position, defined as (x+1,y)
    """
    (x,y) = original_position
    return (x+1,y)

def get_position_left(original_position):
    """
    Given a position (x,y) returns the position to the left of the original position, defined as (x-1,y)
    """
    (x,y) = original_position
    return (x-1,y)

def reset_game(pyrat,game,starting_point,end_point):
    pyrat.pieces = 1
    game.pieces_of_cheese = [end_point]
    game.player1_location = starting_point
    game.history["pieces_of_cheese"] = [game.convert_cheeses()]
    game.history["player1_location"] = [list(starting_point)]
    game.play_match()
    return game

def create_walk_from_parents(parent_dict,source_node,end_node):
    
    route = list()
    next_node = end_node
    while next_node != source_node:
        route.append(next_node)
        next_node = parent_dict[next_node]
    return list(reversed(route))
   
def get_direction(source_node,end_node):
    if get_position_above(source_node) == end_node:
        return MOVE_UP
    elif get_position_below(source_node) == end_node:
        return MOVE_DOWN
    elif get_position_left(source_node) == end_node:
        return MOVE_LEFT
    elif get_position_right(source_node) == end_node:
        return MOVE_RIGHT
    else:
        raise Exception("Nodes are not connected")

def walk_to_route(walk,source_node):
    
    route = list()
    for node in walk:
        direction = get_direction(source_node,node)
        route.append(direction)
        source_node = node
    return route

def is_labeled(labeled_vertices,vertex):
    return vertex in labeled_vertices

def add_to_labeled_vertices(labeled_vertices,vertex):
    labeled_vertices.append(vertex)

def heap_pop(heap):

    node,weight,parent = heap.pop(0)
    
    return (node, weight, parent)


def heap_add_or_replace(heap, triplet):
    
    add=False
    if(len(heap)==0):
        heap.append(triplet)
    
    else:
        index=len(heap)
        for i in range(len(heap)):
            if(heap[i][0]==triplet[0]):
                
                if(heap[i][1]<=triplet[1]):
                    return 0
                else:
                    heap.pop(i)
                    if(add==False):
                        index=i
                    break
                        
            if(add==False):
                if(heap[i][1]>triplet[1]):
                    index=i
                    add=True
             
        heap.insert(index,triplet)

def Dijkstra(maze_graph,sourceNode):
    # Variable storing the labeled vertices nodes not to go there again
    labeled_vertices = list()
    
    # Stack of nodes
    heap = list()
    
    #Parent Dictionary
    parent_dict = dict()
    # Distances 
    distances = dict()
    
    # First call
    initial_tuple = (sourceNode, 0, sourceNode)#Node to visit, distance from origin, parent
    heap_add_or_replace(heap,initial_tuple)
    while len(heap) > 0:
        # get the tuple  with the smallest weight from heap list using heap_pop function.
        # if tuple is not labeled:
        #     map the obtained parent in tuple as parent of the node.
        #     add node to labeled vertices.
        #     compute distance from initial point to the node.
        #     get all node's neighbor and their corresponding weights.
        #     add all these neighbor to heap.
        #     repeat this process until we visit all graph's nodes.
        #
        # YOUR CODE HERE
        #
        (node, cost, parent) = heap_pop(heap)
        if not (is_labeled(labeled_vertices, node)):
            parent_dict[node] = parent
            add_to_labeled_vertices(labeled_vertices, node)
            distances[node] = cost
            for neighbor in maze_graph[node]:
                if not (is_labeled(labeled_vertices, neighbor)):
                    heap_add_or_replace(heap, (neighbor, cost + maze_graph[node][neighbor], node))
    
    return labeled_vertices, parent_dict, distances

def A_to_B(maze_graph,node_source,node_end):
    
    labeled_vertices,parent_dict,_ = Dijkstra(maze_graph,node_source)
    walk = create_walk_from_parents(end_node=node_end,source_node=node_source,parent_dict=parent_dict)
    return walk_to_route(walk,node_source)    