

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


def fifo(l, requests, omega, tau): 
    etage = 0 #Etage de l'ascenseur avant de commencer
    temps = 0
    for r in requests :
        temps = max(r[0], temps) # On doit attendre la prochaine requête si elle n'est pas encore arrivée
        if r[2] == 'e' :
            temps += omega*etage + omega*r[1] + 2*tau
            etage = r[1]
        else :
            temps += omega*abs(etage - r[1]) + omega*r[1] + 2*tau
    return temps 




