import heapq
from scipy.stats import randint, expon, bernoulli
from algos import *

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
        self.sr = sr
        self.etage = etage

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
        b = bernoulli.rvs(0.5)
        d = expon.rvs(LAMBDA)
        e = randint.rvs(1, L+1)
        if b==0:
            next = Event_arrival(self.time+d, Request(self.request.id+1,'s', e))
        else :
            next = Event_arrival(self.time+d, Request(self.request.id+1,'r', e))
        heapq.heappush(sys.echeancier, (next.time, next)) 

        #Création de l'évènement satisfaction de la requête
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
        self.id = i
        
    def action(self, sys):
        if sys.queue == []:
            sys.ascenseur.idle = True
        else :
            etage, temps = fifo(sys)
            sys.ascenseur.etage = etage
            request = sys.queue.pop(0)
            satisfaction = Event_satisfaction(self.time+temps, request.id)
            heapq.heappush(sys.echeancier, (satisfaction.time, satisfaction))
        

sys = System()
e_fin = Event_end(100)
heapq.heappush(sys.echeancier, (e_fin.time, e_fin))

request = Request(0, 's', 2)
e_debut = Event_arrival(0, request)
heapq.heappush(sys.echeancier,(e_debut.time, e_debut))

while sys.echeancier[0][1].type != "fin":
        (time, e) = heapq.heappop(sys.echeancier)
        e.action(sys)

