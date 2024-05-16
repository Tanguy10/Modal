import heapq
from scipy.stats import randint, expon, bernoulli
import algos
from instance import create_request
from statistics import mean

LAMBDA = 1 #Sert pour la loi exponentielle
L = 10 #Nombre d'étages
OMEGA = 1 #Temps mis par l'ascenseur pour passer d'un étage au suivant
TAU = 1 #Temps mis par l'ascenseur pour charger ou décharger un colis

class Ascenseur(object):
    def __init__(self):
        self.idle = True
        self.etage = randint.rvs(0, L+1)
        # self.etage = 2

class System(object):
    def __init__(self):
        self.echeancier = []
        self.queue = [] #File d'attente
        self.ascenseur = Ascenseur() 
        
class Request(object):
    def __init__(self, i, sr, etage):
        self.id = i #Identifiant de la requête
        self.sr = sr #'s' si stockage, 'r' si retrieval
        self.etage = etage #etage correspondant

class Event(object):
    def __init__(self, time) :
        self.time = time #Temps de réalisation
        self.type = " " #Nature de la requête (début/fin/arrivée d'une requête/satisfaction d'une requête)

class Event_end(Event):
    """Evenement fin"""
    def __init__(self, time):
        self.time = time
        self.type = "fin"

class Event_arrival(Event):
    """Arrivée d'une requête"""
    def __init__(self, time, request):
        self.time = time
        self.type = "arrival"
        self.request = request

    
    def action(self, sys):
        sys.queue.append(self.request) #Ajout à la file d'attente

        #Création d'un nouvel évènement d'arrivée d'une requête
        d = expon.rvs(LAMBDA) # Temps d'attente pour la prochaine requête
        next_request = create_request(self.request.id + 1) # Prochaine requête
        next = Event_arrival(self.time+d, next_request) # Evènement associé
        heapq.heappush(sys.echeancier, (next.time, next)) 

        #Création de l'évènement satisfaction de la requête dans le cas où l'ascenseur est libre
        if sys.ascenseur.idle :
            if self.request.sr == 's':
                temps_satisfaction = (sys.ascenseur.etage + self.request.etage)*OMEGA + 2*TAU
                sys.ascenseur.idle = False
                sys.ascenseur.etage = self.request.etage
            else :
                temps_satisfaction = (abs(sys.ascenseur.etage - self.request.etage) + self.request.etage)*OMEGA +2*TAU
                sys.ascenseur.idle = False
                sys.ascenseur.etage = 0
            satisfaction = Event_satisfaction(self.time+temps_satisfaction, self.request.id)
            heapq.heappush(sys.echeancier, (satisfaction.time, satisfaction))
                
            

class Event_satisfaction(Event):
    """Satisfaction d'une requête"""
    def __init__(self, time, i):
        self.time = time
        self.type = "satisfaction"
        self.id = i #Identifiant de la requête satisfaite
        
    def action(self, sys):
        if sys.queue == []: #Si la file d'attente est vide, l'ascenseur est libre
            sys.ascenseur.idle = True 
        else : #Sinon, on exécute un algo
            sys.ascenseur.idle = False 
            etage, temps = algos.fifo(sys)
            request = sys.queue.pop(0)

            sys.ascenseur.etage = etage #Ascenseur mis en position finale
            satisfaction = Event_satisfaction(self.time+temps, request.id)
            heapq.heappush(sys.echeancier, (satisfaction.time, satisfaction))
        


TOTAL_DURATION=100 #Temps d'un run
NBR_RUNS = 10

waiting_times_run = []
for i in range(NBR_RUNS) :
    # random.seed(i) 

    sys = System() #Création du système
    e_fin = Event_end(TOTAL_DURATION) # Evènement de fin
    heapq.heappush(sys.echeancier, (e_fin.time, e_fin)) #Ajout de la fin à l'échéancier

    request = create_request(0) #Première requête
    waiting_times_requests = [0]
    e_debut = Event_arrival(0, request) #Début de la simulation 
    heapq.heappush(sys.echeancier,(e_debut.time, e_debut))

    while sys.echeancier[0][1].type != "fin": #Tant qu'on n'est pas à la fin
        time, e = heapq.heappop(sys.echeancier) 
        e.action(sys)
        if e.type == 'satisfaction':
            waiting_times_requests[e.id] += e.time # Temps d'attente de la requête
        elif e.type == 'arrival':
            waiting_times_requests.append(-e.time)
    # print(waiting_times_requests)
    
    i = 0
    while waiting_times_requests[i] >=0 :
        i+= 1
    waiting_times_run.append(mean(waiting_times_requests[:i]))
print(mean(waiting_times_run))
