import instance
import networkx as nx
import itertools


def resolution_statique(sys):
    """Résolution du problème offline en version statique"""
    from simulateur import L, TAU, OMEGA 
    etage_dep = sys.ascenseur.etage
    nb_entrees = len(sys.queues[0])
    nb_sorties = [len(sys.queues[i]) for i in range(1, L+1)]

    # entrees, sorties = [],[]
    # for r in requests :
    #     if r[2] == 'e': 
    #         entrees.append(r[1]) #r[0] ne nous intéresse pas pour le problème statique
    #     else :
    #         sorties.append(r[1])
    # nb_entrees, nb_sorties = len(entrees), len(sorties)

    # On crée un graphe, la résolution statique est un problème de plus court chemin
    G = nx.DiGraph()

    # Les états sont [i,j_1, ..., j_L,k] avec i les requêtes d'entrées traitées, j_i les requêtes de sorties de l'étage i 
    # et k l'étage où est l'ascenseur après la requête qu'il vient de traiter
    states = itertools.product(range(nb_entrees+1), *(range(nb_sorties[i]+1) for i in range(L)), range(L+1))
    for state in states :
        G.add_node(state)
    print("Liste des noeuds créés:")
    print(list(G.nodes()))

    # Les arêtes sont [i,j_1,...,j_L,l] -> [i+1, j_1, ..., j_L, s_{i+1}] 
    # ou [i, j_1, ..., j_n, ..., j_L,l] -> [i, j_1, ..., j_{n}+1, ..., j_L, 0]
    for state in G.nodes():
        i, *j, k = state

        if i < nb_entrees:
            next_state = (i+1, *j, sys.queues[0][i].etage)
            G.add_edge(state, next_state, weight = 2*TAU + OMEGA * (k + sys.queues[0][i].etage))
        
        for n in range(L):
            if j[n] < nb_sorties[n]:
                j_copy = j.copy()
                j_copy[n] += 1
                next_state = (i, *j_copy, 0)
                G.add_edge(state, next_state, weight = 2*TAU + OMEGA * (abs(n+1-k)+(n+1)))


    # Résolvons désormais le problème du plus court chemin entre le noeud (0,0,etage_dep) et le noeud (nb_sorties,nb_entrees,)
    # nx.dijkstra_path_length(G,source = (0,0,0), target = (nb_sorties,nb_entrees,))
    # nx.multi_source_dijkstra_path_length()
    longueurs, chemins = nx.single_source_dijkstra(G, source = (0,*[0 for i in range(L)], etage_dep))

    # Noeuds d'arrivée d'intérêt
    noeuds_arrivee = [(nb_entrees, *nb_sorties,k) for k in range(L+1)]

    # Afficher les chemins et longueurs pour les nœuds d'arrivée spécifiés
    noeud_sortie_min = None
    temps_sortie_min = float('inf')
    chemin_min = None
    
    for arrivee in noeuds_arrivee:
        if arrivee in longueurs and temps_sortie_min > longueurs[arrivee]:
            noeud_sortie_min = arrivee
            temps_sortie_min = longueurs[noeud_sortie_min]
            chemin_min = chemins[noeud_sortie_min]

    return chemin_min
    # Renvoyons une liste qui donne les requêtes qui ont été traitées pour le temps optimale
    # requetes_accomplies=[]
    # for i in range(1,len(chemins)):
    #     if chemins[i][2]==0:
    #         requetes_accomplies.append('s')
    #     else :
    #         requetes_accomplies.append('e')
    # # On renvoie le temps mis et l'étage à l'arrivée 
    # return temps_sortie_min, noeud_sortie_min[2], requetes_accomplies


def fifo(sys): 
    """Renvoie l'étage de la requête à traiter (sous forme d'une liste de longueur 1 pour coller avec le format de ignore)"""    
    # On détermine les requêtes pouvant être choisis
    possible_requests = []
    for q in sys.queues:
        if q != []:
            possible_requests.append(q[0])
    # Puis celle qui est arrivée en premier
    request = possible_requests[0]
    for r in possible_requests:
        if request.arrival > r.arrival:
            request = r
    
    if request.sr == 's' :
        return [0] 
    else :
        return [request.etage] 

    

def replan(sys): 
    """Renvoie l'étage de la requête à traiter"""
    from simulateur import L, TAU, OMEGA
    
    chemin = resolution_statique(sys)
    for n in range(L+1):
        if chemin[1][n] != 0:
            return [n]
    
