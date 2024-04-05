

def resolution_offline(l, entrées, sorties, omega, tau):
    """Résolution du problème offline"""
    nb_entrées = len(entrées)
    nb_sorties = len(sorties)
    # Les états sont (i,j,etage,colis)
    etats = [[[[0 for etage in range(l+1)] for _ in range(3)] for j in range(nb_sorties)] for i in range(nb_entrées)]
    for i in range(nb_entrées):
        for j in range(nb_sorties):
            for k in range(3):
                if k == 0: #Ascenseur vide
                    for etage in range(l+1):
                        etats[i][j][k][etage] = max(etats[i-1][j][1][entrées[i]] + tau + omega*abs(entrées[i] - etage),
                                                     etats[i][j-1][2][0] + tau + omega*etage)
                elif k == 1: #Ascenseur avec une requête d'entrée donc montée
                    etats[i][j][k][0] = etats[i][j][0][0] + tau
                elif k == 2: #Ascenseur avec requête de sortie
                    etats[i][j][k][sorties[j]] = etats[i][j][0][sorties[j]] + tau