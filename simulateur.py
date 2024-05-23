import heapq
from scipy.stats import randint, expon
import algos
from instance import create_request
from statistics import mean
import matplotlib.pyplot as plt

LAMBDA = 0.01 # Sert pour la loi exponentielle
L = 10  # Nombre d'étages
OMEGA = 1  # Temps mis par l'ascenseur pour passer d'un étage au suivant
TAU = 1  # Temps mis par l'ascenseur pour charger ou décharger un colis

class Ascenseur(object):
    def __init__(self):
        self.idle = True
        self.etage = randint.rvs(0, L + 1)

class System(object):
    def __init__(self):
        self.echeancier = []
        self.requests = [] # La liste des requêtes
        self.queues = [[] for i in range(L+1)]  # Files d'attente, queues[0] est la file des colis voulant rentrer, queues[i] est la file des colis voulant sortir de l'étage i
        self.ascenseur = Ascenseur()

class Request(object):
    def __init__(self, i, sr, etage):
        self.id = i  # Identifiant de la requête
        self.sr = sr  # 's' si stockage, 'r' si retrieval
        self.etage = etage  # étage correspondant
        self.arrival = -1 # Temps d'arrivée, vaut -1 initialement
        self.satisfaction_time = -1 # Temps de satisfaction, vaut -1 tant que la requête n'est pas satisfaite

class Event(object):
    def __init__(self, time):
        self.time = time  # Temps de réalisation
        self.type = " "  # Nature de la requête (début/fin/arrivée d'une requête/satisfaction d'une requête)

    def __lt__(self, other):
        return self.time < other.time

class Event_end(Event):
    """Evénement fin"""
    def __init__(self, time):
        super().__init__(time)
        self.type = "fin"

class Event_arrival(Event):
    """Arrivée d'une requête"""
    def __init__(self, time):
        super().__init__(time)
        self.type = "arrival"

    def action(self, sys):
        request = sys.requests[-1] # Dernière requête 
        request.arrival = self.time # On actualise le temps d'arrivée
        # sys.requests.append(request)  # Ajout à la file d'attente
        d = expon.rvs(scale = 1/LAMBDA)  # Temps d'attente pour la prochaine requête
        next_request = create_request(len(sys.requests))  # Prochaine requête
        sys.requests.append(next_request) # Ajout de cette requête à la liste des requêtes
        next = Event_arrival(self.time + d)  # Evénement associé
        heapq.heappush(sys.echeancier, (next.time, next)) # Prochaine arrivée dans l'échéancier

        if sys.ascenseur.idle:
            if request.sr == 's':
                temps_satisfaction = (sys.ascenseur.etage + request.etage) * OMEGA + 2 * TAU
                sys.ascenseur.idle = False
                sys.ascenseur.etage = request.etage
            else:
                temps_satisfaction = (abs(sys.ascenseur.etage - request.etage) + request.etage) * OMEGA + 2 * TAU
                sys.ascenseur.idle = False
                sys.ascenseur.etage = 0
            satisfaction = Event_satisfaction(self.time + temps_satisfaction, request.id)
            heapq.heappush(sys.echeancier, (satisfaction.time, satisfaction)) # Satisfaction de la requête
        else :
            if request.sr == 's':
                sys.queues[0].append(request) # Ajout à la file d'attente
            else :
                sys.queues[request.etage].append(request)

class Event_satisfaction(Event):
    """Satisfaction d'une requête"""
    def __init__(self, time, i):
        super().__init__(time)
        self.type = "satisfaction"
        self.id = i  # Identifiant de la requête satisfaite

    def action(self, sys):
        sys.requests[self.id].satisfaction_time = self.time
        # On détermine si les files d'attente sont vides 
        if sum([len(q) for q in sys.queues]) == 0: 
            sys.ascenseur.idle = True # Dans ce cas l'ascenseur est libre
        else:  # Sinon, on exécute un algo
            sys.ascenseur.idle = False
            etage_courant = sys.ascenseur.etage
            temps_courant = self.time
            indices = algos.replan(sys) # Suite des requêtes à traiter
            for i in indices :
                request = sys.queues[i].pop(0)
                if request.sr == 's':
                    temps_courant += OMEGA*(etage_courant + request.etage) + 2*TAU
                    etage_courant =  request.etage
                else :
                    temps_courant += OMEGA*(abs(sys.ascenseur.etage - request.etage) + request.etage) + 2*TAU
                    etage_courant = 0 
                satisfaction = Event_satisfaction(temps_courant, request.id) 
                heapq.heappush(sys.echeancier, (satisfaction.time, satisfaction)) # Ajout de la satisfaction à l'échéancier
            sys.ascenseur.etage = etage_courant  # Ascenseur mis en position finale
            
            
TOTAL_DURATION = 1000  # Temps d'un run
TRANSIENT_DURATION = 1000 # Régime transitoire
NBR_RUNS = 5



sojourn_times_run = []
for i in range(NBR_RUNS):
    sys = System()  # Création du système
    e_fin = Event_end(TOTAL_DURATION)  # Evénement de fin
    heapq.heappush(sys.echeancier, (e_fin.time, e_fin))  # Ajout de la fin à l'échéancier

    request = create_request(0)  # Première requête
    sys.requests.append(request)
    e_debut = Event_arrival(0)  # Début de la simulation
    heapq.heappush(sys.echeancier, (e_debut.time, e_debut))

    while sys.echeancier[0][1].type != "fin":  # Tant qu'on n'est pas à la fin
        (time, e) = heapq.heappop(sys.echeancier)
        e.action(sys)

    sojourn_times_requests = [] # Temps de séjour par requête
    sojourn_mean = []
    for r in sys.requests:
        if r.satisfaction_time != -1:
            sojourn_times_requests.append(r.satisfaction_time - r.arrival)
            sojourn_mean.append(sum(sojourn_times_requests)/(len(sojourn_mean)+1))
    sojourn_times_run.append(sojourn_mean)


plt.clf()
for s in sojourn_times_run:
    plt.plot(s)

plt.savefig('result.png')

    
