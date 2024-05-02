import heapq
from scipy.stats import randint, expon, bernoulli

LAMBDA = 1 #Sert pour la loi exponentielle
L = 10 #Nombre d'étage
OMEGA = 1 #Temps mis par l'ascenseur pour passer d'un étage au suivant
TAU = 1 #Temps mis par l'ascenseur pour charger ou décharger un colis

class Ascenseur(object):
    def __init__(self):
        self.idle = True
        self.etage = randint(0, L+1)

echeancier = []
queue = [] #File d'attente
ascenseur = Ascenseur() 

# class Request(object):
#     def __init__(self, i):
#         self.id = i #Identifiant de la requête

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
    def __init__(self, time, sr, etage):
        self.time = time
        self.type = "arrival"
        self.sr = sr #Stockage ou retrieval 
        self.etage = etage #Etage de la requête
    
    def action(self):
        queue.append((self.sr,self.etage)) #Ajout à la file d'attente

        #Création d'un nouvel évènement d'arrivée d'une requête
        b = bernoulli.rvs(0.5)
        d = expon.rvs(LAMBDA)
        e = randint.rvs(1, L+1)
        if b==0:
            next = Event_arrival(self.time+d, 's', e)
        else :
            next = Event_arrival(self.time+d, 'r', e)
        heapq.heappush(echeancier, (next.time, next)) 

        #Création de l'évènement satisfaction de la requête
        if ascenseur.idle :
            if self.sr == 's':
                temps_satisfaction = ascenseur.etage + self.etage
                ascenseur.idle = False
                ascenseur.etage = self.etage
            else :
                temps_satisfaction = abs(ascenseur.etage - self.etage) + self.etage
                ascenseur.idle = False
                ascenseur.etage = 0
            satisfaction = Event_satisfaction(self.time+temps_satisfaction, self.sr, self.etage)
            heapq.heappush(echeancier, (satisfaction.time, satisfaction))
                
            

class Event_satisfaction(Event):
    """Satisfaction d'une requête"""
    def __init__(self, time, sr, etage):
        self.time = time
        self.type = "satisfaction"
        self.sr = sr
        self.etage = etage
