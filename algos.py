from simulateur import *
from instance import *

def resolution_statique(l, requests, omega, tau):
    """Résolution du problème offline"""
    entrees, sorties = [],[]
    for r in requests :
        if r[2] == 'e': 
            entrees.append(r[1]) #r[0] ne nous intéresse pas pour le problème statique
        else :
            sorties.append(r[1])
    nb_entrees, nb_sorties = len(entrees), len(sorties)

    # Les états sont (i,j,l) avec i les requêtes d'entrées traitées, j les requêtes de sorties
    # et l l'étage où est l'ascenseur après la requête qu'il vient de traiter
    etats = [[[0 for _ in range(l+1)] for _ in range(nb_sorties)] for _ in range(nb_entrees)]

    # Les arêtes sont (i,j,l) -> (i+1, j, s_{i+1}) et (i,j,l) -> (i, j+1, 0)


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





