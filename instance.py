import numpy as np
from scipy.stats import randint, expon, bernoulli


def offline(l=5, T=1000):
    """Crée une instance sous forme d'une liste de requêtes contenant un triplet 
    (temps d'arrivée, étage, entrée/sortie) jusqu'au temps T"""
    requests = []
    t = 0 #Le compteur temps
    while t < T:
        d = expon.rvs() #Pour l'instant lambda = 1
        t += d #On avance dans le temps
        etage = randint.rvs(1, l+1) #L'étage de la requête, on suppose que l'étage est non nul pour simplifier
        b = bernoulli.rvs(0.5) #Permet de choisir entre entrée ou sortie
        if b==0 :
            requests.append((t, etage, 'e'))
        else :
            requests.append((t, etage, 's'))
    return requests

def online(l,T,lamda):
    size = 1000  # Nombre de tirages
    # Tirer de la distribution de Poisson
    tirages_poisson = np.random.poisson(lamda, size)
    tirages_bernoulli =  bernoulli.rvs(0.5, size=size)
    for i in range(size):
        if tirages_bernoulli[i]==0 :
            tirages_bernoulli[i] = 'e'
        else : 
            tirages_bernoulli[i] = 's'
    return tirages_bernoulli,tirages_poisson

