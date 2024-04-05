import numpy as np
from scipy.stats import randint


def offline(n, l):
    """Crée une instance sous forme de deux listes, une pour les entrées et l'autre pour les sorties
    n est le nombre de requêtes d'entrées et de sortie
    l est le nombre d'étages"""
    entrées, sorties = []
    for i in range(n) :
        etage = randint(0, l+1)
        entrées.append(etage)
        etage = randint(0, l+1)
        sorties.append(etage)
    return entrées, sorties