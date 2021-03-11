TEAM_NAME = "Tournoi"
####### Ce programme test le voyageur de commerce qui calcule localement le meilleur chemin en imposant de s'arrêter à une position 
###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

###############################
# Please put your imports here
import sys
import random
from random import shuffle
from math import exp
###############################
# Please put your global variables here
nbTurn = 0
chemin = []

###############################
# Preprocessing function
# Function that returns the location above#
def aboveOf(location):
    return((location[0],location[1]+1))

# Function that returns the location below#
def belowOf(location):
    return((location[0],location[1]-1))

# Function that returns the location at left#
def leftOf(location):
    return((location[0]-1,location[1]))

# Function that returns the location at right#
def rightOf(location):
    return((location[0]+1,location[1]))
    
CheminToCheese= []
meilleur_chemin=[]

#Retourne la suite des fromages à suivre en cherchant à chaque fois le fromage le plus proche:  
def glouton(meta_distances,piecesOfCheese,départ):
    sommet_départ=départ
    cheeses_restants=[cheese for cheese in piecesOfCheese]
    pieces=[départ]+[cheese for cheese in piecesOfCheese]
    ordre_cheeses=[]
    
    cheese,distance=piecesOfCheese[0],meta_distances[sommet_départ][piecesOfCheese[0]]
    #Tant que la liste des fromages n'est pas vide, le programme cherche le fromage le plus proche
    while cheeses_restants != []:
        #Compteur: distance entre l'élement i et l'élélement i+1 de piecesOfCheese:
        cheese,distance=cheeses_restants[-1],meta_distances[sommet_départ][cheeses_restants[-1]]

        #Cherche le fromage le plus proche
        for fromage in cheeses_restants:

            distance_fromage=meta_distances[sommet_départ][fromage]

            if distance_fromage<distance:
                cheese,distance=fromage,distance_fromage

        ordre_cheeses=ordre_cheeses+[cheese]
        sommet_départ=cheese
        cheeses_restants.remove(cheese)
    return(ordre_cheeses)

def exhaus(piecesOfCheese,meta_distance,meta_chemin,playerLocation,fromage_final):
    Noeuds=[sommet for sommet in piecesOfCheese]
    n=0
    meilleur_chemin=[]
    mieux=10000

    def exhaustif(restants,sommet,chemin,poids,graphe,fromage_final):
        nonlocal mieux
        nonlocal meilleur_chemin
        nonlocal n
        if restants==[]:
            if poids<mieux:
                mieux=poids
                meilleur_chemin=chemin       
        else:

            for Noeud in graphe[sommet].keys():

                if Noeud in restants:
                    otherNodes = [i for i in restants if i != Noeud]
                    if fromage_final in chemin:
                        
                        if not chemin.index(fromage_final)==n:

                            return
                        else:
                            n=n+1
                    exhaustif(otherNodes,Noeud,chemin+[Noeud],poids+graphe[sommet][Noeud],graphe,fromage_final)
    exhaustif(Noeuds,playerLocation,[],0,meta_distance,fromage_final)

    return (meilleur_chemin)
#Crée un métagraphe:
def meta_graphe(graphe,piecesOfCheese,sommet_départ):
    #Liste des Noeuds (les cheese et (0,0))
    Noeuds=[sommet_départ]+piecesOfCheese
    #Metagraphe des distances
    meta_distance={}
    #Metagraphe des chemins:
    meta_chemins={}

    n=len(Noeuds)
    for sommeti in Noeuds:
        for sommetj in Noeuds:
            if sommeti!=sommetj:
            
                Distancesi,Routagei=dijikstra_distances(graphe,sommeti)
                distance=Distancesi[sommetj]
                chemin=Chemin(sommetj,sommeti,Routagei)
                if sommeti in meta_distance.keys():
                    meta_distance[sommeti][sommetj]=distance
                    meta_chemins[sommeti][sommetj]=chemin
                else:
                    meta_distance[sommeti]={sommetj:distance}
                    meta_chemins[sommeti]={sommetj:chemin}    
                
    return [meta_distance,meta_chemins]
#Transforme un routage en un chemin:
def Chemin(sommet_arrivé,sommet_départ,routage):
    Parcours=routage
    cheese=sommet_arrivé
    Chemin=[cheese]
    position=cheese
    while position!=sommet_départ:
        Chemin=[Parcours[position]]+Chemin
        position=Parcours[position]
    Chemin.remove(cheese)
    return(Chemin)
#Retourne une liste de deux éléments, un dictionnaire de distances, et une table de routage à partir d'un sommet de départ:        
def dijikstra_distances(graphe,sommet_départ):
        infini=10000
        priorité=[]
        priorité=priorité+[(sommet_départ,0)]
        distances={}
        for sommets in graphe:
            distances[sommets]=infini
        distances[sommet_départ]=0
        routage={}
        i=0
        while priorité != []:
                (sommet_courant,distance)=priorité.pop(0)
                
                for voisin in graphe[sommet_courant]:
                        dist_par_courant = distance + graphe[sommet_courant][voisin]
                        if distances[voisin]>dist_par_courant:
                                distances[voisin]=dist_par_courant
                                priorité=priorité+[(voisin,dist_par_courant)]
                                routage[voisin]=sommet_courant
                                i=i+1

        return [distances,routage]

cheeses=[]
#Reçoit l'ordre des bouts de fromage et créer tout le chemin:
def Chemin_global(meilleur_chemin,meta_chemins,playerLocation):
    
    meilleur_chemin=[playerLocation]+meilleur_chemin
    chemin_global=[]
    
    for i in range(len(meilleur_chemin)-1):
        #Les mêmes élements sont présents dans la valeur de deux clés successives, il faudra enlever une
        chemin_global=chemin_global+meta_chemins[meilleur_chemin[i]][meilleur_chemin[i+1]]
    chemin_global=chemin_global+[meilleur_chemin[-1]]
    
    return(chemin_global)


meta_distances={}
meta_chemins={}
import time
start_time=0
#Retourne l'ordre des frommages en fonction de leur distances de la case de départ:
def Fromages_proches(piecesOfCheese,playerLocation,meta_distances):
    Ordre=[]
    Fromages={}
    for cheese in meta_distances[playerLocation].keys():
        Fromages[cheese]=meta_distances[playerLocation][cheese]
    Distances=[]
  
    while Fromages!={}:        
        fromage_plus_proche=min(Fromages)
        del Fromages[fromage_plus_proche]
        Ordre=Ordre+[fromage_plus_proche]
    return(Ordre)
trajet=[]
T=0
def recuit_simule(piecesOfCheese_Depart,meta_distances,playerLocation):
    Time_recuit=time.time()
    global trajet
    global T
    N = len(piecesOfCheese_Depart)    # nombre de villes

    # paramètres de l'algorithme de recuit simulé
    T0 = 1.0
    Tmin = 1e-2
    tau = 1e3

    # fonction de calcul de l'énergie du système, égale à la distance totale
    # du trajet selon le chemin courant
    

    def somme_chemin(meta_distances,playerLocation):
        global trajet
        Distance=meta_distances[playerLocation][trajet[1]]
        n=len(trajet)
        for i in range(1,n):
            Distance=Distance+meta_distances[trajet[i-1]][trajet[i]]
        return(Distance)

    # fonction de fluctuation 
    def Fluctuation(i,j):
        global trajet
        Min = min(i,j)
        Max = max(i,j)
        trajet[Min:Max] = trajet[Min:Max].copy()[::-1]
        return

    # fonction d'implémentation de l'algorithme de Metropolis
    def Metropolis(Distance1,Distance2):
        global T
        if Distance1 <= Distance2:
            Distance2 = Distance1  # énergie du nouvel état = énergie système
        else:
            dE = Distance1-Distance2
            if random.random() > exp(-dE/T): # la fluctuation est retenue avec  
                Fluctuation(i,j)              # la proba p. sinon retour trajet antérieur si dE tres grand, proba presque sur > exp(-dE/T) et change.
            else:
                Distance2 = Distance1 # la fluctuation est retenue 
        return Distance2
        
        
    
    # initialisation des listes d'historique
    Henergie = []     # énergie
    Htemps = []       # temps
    HT = []           # température



    # défintion du trajet initial :
    trajet = [playerLocation]+glouton(meta_distances,piecesOfCheese_Depart,playerLocation)
    trajet_init = trajet.copy()

    # calcul de l'énergie initiale du système (la distance initiale à minimiser)
    Ec = somme_chemin(meta_distances,playerLocation)
    print("Distance initiale",Ec)
    

    # boucle principale de l'algorithme de recuit simulé
    t = 0
    T = T0
    while T > Tmin:
        # choix de deux fluctuations différentes au hasard
        i = random.randint(1,N-1)
        j = random.randint(1,N-1)
        if i == j: continue
            
        # création de la fluctuation et mesure de l'énergie
        Fluctuation(i,j) 
        Ef = somme_chemin(meta_distances,playerLocation) 
        Ec = Metropolis(Ef,Ec)
        
        # application de la loi de refroidissement    
        t += 1
        
        T = T0*exp(-t/tau)  

        # historisation des données
        if t % 10 == 0:
            Henergie.append(Ec)
            Htemps.append(t)
            HT.append(T)
        
    print("Temps_recuit=",time.time()-Time_recuit)
    print("Distance_finale",somme_chemin(meta_distances,playerLocation))
    print(len(Htemps))
    return(trajet)


def somme_chemin(piecesOfCheese,meta_distances,playerLocation):
    Distance=meta_distances[playerLocation][piecesOfCheese[0]]
    n=len(piecesOfCheese)
    for i in range(1,n):
        Distance=Distance+meta_distances[piecesOfCheese[i-1]][piecesOfCheese[i]]
    return(Distance)





def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
        piecesOfCheese=list(set(piecesOfCheese))
        global meta_distances
        global meta_chemins
        Location=playerLocation
        ordre_voyageur=[]
        n=len(piecesOfCheese)
        global start_time
        start_time = time.time()

        global cheeses
        global mieux
        global CheminToCheese
        cheeses=piecesOfCheese
        #CheminToCheese=exhaustif(cheeses,(0,0),[],0,mazeMap)
        
        meta_distances,meta_chemins=meta_graphe(mazeMap,piecesOfCheese,playerLocation)
        
        #Réordonne les fromages:
        ordre_voyageur=recuit_simule(piecesOfCheese,meta_distances,playerLocation)[1:]
            #Location=ordre_voyageur[-1]
        #Retourne le chemin absolu entre les bouts de frommage:
        CheminToCheese=Chemin_global(ordre_voyageur,meta_chemins,playerLocation)[1:]

def postprocessing(mazeMap, mazewidth, mazeheight, player1_location, player2_location, score1, score2, pieces_of_cheese, turn_time):
    global start_time
    print("score = ",score1,"time = ",time.time()-start_time)
    

compteur_adversaire=0  

def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global compteur_adversaire
    global CheminToCheese
    global meta_chemins
    global meta_chemins

    """compteur_adversaire!=opponentScore:
    meta_distances,meta_chemins=meta_graphe(mazeMap,piecesOfCheese,playerLocation)

    Liste_cheeses=Fromages_proches(piecesOfCheese,playerLocation,meta_distances)
    Liste_restreinte=Liste_cheeses[:7]
    fromage_final=Liste_restreinte[-1]  
    ordre_voyageur=exhaus(Liste_restreinte,meta_distances,meta_chemins,playerLocation,fromage_final)
    CheminToCheese=Chemin_global(ordre_voyageur,meta_chemins,playerLocation)[1:]
    compteur_adversaire=opponentScore"""

    if CheminToCheese != []:
        nextLocation=CheminToCheese.pop(0)
        
        if nextLocation==aboveOf(playerLocation):
            return MOVE_UP
        elif nextLocation==belowOf(playerLocation):
            return MOVE_DOWN
        elif nextLocation==rightOf(playerLocation):
            return MOVE_RIGHT
        elif nextLocation==leftOf(playerLocation):
            return MOVE_LEFT
    else:
        return("Game finished")  
        
        
