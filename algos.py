LAMBDA = 1 #Sert pour la loi exponentielle
L = 10 #Nombre d'étage
OMEGA = 1 #Temps mis par l'ascenseur pour passer d'un étage au suivant
TAU = 1 #Temps mis par l'ascenseur pour charger ou décharger un colis
from instance import *
import networkx as nx


def resolution_statique(l, requests, omega, tau):
    """Résolution du problème offline en version statique"""
    entrees, sorties = [],[]
    for r in requests :
        if r[2] == 'e': 
            entrees.append(r[1]) #r[0] ne nous intéresse pas pour le problème statique
        else :
            sorties.append(r[1])
    nb_entrees, nb_sorties = len(entrees), len(sorties)
    G = nx.Digraph()

    # Les états sont (i,j,k) avec i les requêtes d'entrées traitées, j les requêtes de sorties
    # et k l'étage où est l'ascenseur après la requête qu'il vient de traiter
    for k in range(l+1):
        for j in range(nb_sorties):
            for i in range(nb_entrees) :
                G.add_nodes((i,j,k))
    # Les arêtes sont (i,j,l) -> (i+1, j, s_{i+1}) et (i,j,l) -> (i, j+1, 0)
    for k in range(l+1):
        for j in range(nb_sorties):
            for i in range(nb_entrees) :
                if i+1<nb_entrees:
                    G.add_edge((i,j,k),(i+1, j, entrees[i]), weight = 2*tau + omega * (k + entrees[i]))
                if j+1 < nb_sorties : 
                    G.add_edge((i,j,k),(i,j+1,0), weight = 2*tau + omega * (abs(sorties[j]-k)+sorties[j]) )

    # Résolvons désormais le problème du plus court chemin entre le noeud (0,0,0) et le noeud (nb_sorties,nb_entrees,)
    # nx.dijkstra_path_length(G,source = (0,0,0), target = (nb_sorties,nb_entrees,))
    # nx.multi_source_dijkstra_path_length()
    longueurs, chemins = nx.single_source_dijkstra(G, source = (0,0,0))

    # Noeuds d'arrivée d'intérêt
    noeuds_arrivee = [(nb_entrees,nb_sorties,k) for k in range(l+1)]

    # Afficher les chemins et longueurs pour les nœuds d'arrivée spécifiés
    noeud_sortie_min = (nb_entrees,nb_sorties,0)
    temps_sortie_min = longueurs[(nb_entrees,nb_sorties,0)]
    for arrivee in noeuds_arrivee:
        if temps_sortie_min>longueurs[arrivee] :
            temps_sortie_min = longueurs[arrivee]
            noeud_sortie_min = noeuds_arrivee[arrivee]

    # On renvoie le temps mis et l'étage à l'arrivée 
    return temps_sortie_min, noeud_sortie_min[2]


def fifo(sys): 
    """Renvoie l'étage de fin et le temps mis pour traiter la requête"""
    request = sys.queue[0]
    if request.sr == 's' :
        etage = request.etage
        temps = OMEGA*(sys.ascenseur.etage+request.etage) + 2*TAU
    else :
        etage = 0
        temps = OMEGA*(abs(sys.ascenseur.etage - request.etage) + request.etage) + 2*TAU
    return etage, temps
