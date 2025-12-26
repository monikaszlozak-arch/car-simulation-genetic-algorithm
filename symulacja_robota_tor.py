import pygame
import sys
import math
import numpy as np
import random
import pygame
from collections import deque
import matplotlib.pyplot as plt
from IPython import display
import time
import neat
import json
import pickle
import easygui

clock = pygame.time.Clock()
pygame.init()
okno = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Czołg z obracającym się hitboxem")
font = pygame.font.SysFont(None, 20)
centymetr = 1

class Word:
    """Klasa reprezentująca agenta AI (model, pamięć, trening)."""
    def __init__(self):
        self.epoch = 1000
        self.n_game = 0
        #---------------------------------------------
        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            "config.txt"
        )
        self.population = neat.Population(config) 
        self.population.add_reporter(neat.StdOutReporter(True)) 
        stats = neat.StatisticsReporter() 
        self.population.add_reporter(stats)
        #-----------------------------------------------
        self.e = env()

    def train(self):
        winner = self.population.run(self.eval_population , self.epoch)
        return winner
    def eval_population(self , genomes, config):
        self.e.symulacja(genomes, config)
            
    def write_genome(self , winner):
       with open("best_genome.pkl", "wb") as f: 
           pickle.dump(winner, f)


def point_in_polygon(p, poly):
    x, y = p
    n = len(poly)
    inside = False

    px1, py1 = poly[0]
    for i in range(n + 1):
        px2, py2 = poly[i % n]
        if y > min(py1, py2):
            if y <= max(py1, py2):
                if x <= max(px1, px2):
                    if py1 != py2:
                        xinters = (y - py1) * (px2 - px1) / (py2 - py1) + px1
                    if px1 == px2 or x <= xinters:
                        inside = not inside
        px1, py1 = px2, py2

    return inside

class Sciana:
    def __init__(self, x, y, szer, wys, kat):
        self.x = x
        self.y = y
        self.szer = szer
        self.wys = wys
        self.kat = kat  # w stopniach

    def get_punkty(self):
        rad = math.radians(self.kat)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        dx = self.szer / 2
        dy = self.wys / 2
        punkty = []
        for sx, sy in [(-dx, -dy), (dx, -dy), (dx, dy), (-dx, dy)]:
            rx = self.x + sx * cos_a - sy * sin_a
            ry = self.y + sx * sin_a + sy * cos_a
            punkty.append((rx, ry))
        return punkty

    def draw(self, powierzchnia):
        pygame.draw.polygon(powierzchnia, (150, 150, 150), self.get_punkty())

    def collidepoint(self, punkt):
        # Prosta metoda: sprawdź czy punkt jest w wielokącie
        return point_in_polygon(punkt, self.get_punkty())
def list_sciana(l):
    l2 = []
    for i in l :
        l2.append( Sciana(i[0] , i[1]  ,i[2] , i[3] , i[4]) )
    return l2
class Czolg:
    def __init__(self, x, y, szer, wys):
        self.x = x
        self.y = y
        self.szer = szer
        self.wys = wys
        self.kat = 0
        self.predkosc = 0
        self.obrot = 0

    def update(self, option, sciany):
        stara_x = self.x
        stara_y = self.y
        stary_kat = self.kat

        # Sterowanie gąsienicami
        if option == 0:
            self.predkosc = 8
            self.obrot = 0
        elif option ==2:
            self.predkosc = -8
            self.obrot = 0
        elif option == 1:
            self.predkosc = 0
            self.obrot = 20
        elif option == 3:
            self.predkosc = 0
            self.obrot = -20
        
        else:
            self.predkosc = 0
            self.obrot = 0

        # Ruch
        self.kat += self.obrot
        rad = math.radians(self.kat)
        self.x += math.cos(rad) * self.predkosc
        self.y += math.sin(rad) * self.predkosc  # Y rośnie w dół

        # Kolizja
        if self.kolizja(sciany):

            self.x = stara_x
            self.y = stara_y
            self.kat = stary_kat
            return True
        return False
    def get_punkty(self):
        rad = math.radians(self.kat)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        dx = self.szer / 2
        dy = self.wys / 2
        punkty = []
        for sx, sy in [(-dx, -dy), (dx, -dy), (dx, dy), (-dx, dy)]:
            rx = self.x + sx * cos_a - sy * sin_a
            ry = self.y + sx * sin_a + sy * cos_a
            punkty.append((rx, ry))
        return punkty

    def kolizja(self, sciany):
        punkty = self.get_punkty()
        for sciana in sciany:
            for punkt in punkty:
                if sciana.collidepoint(punkt):
                    return True
        return False

    def get_przod(self):
        rad = math.radians(self.kat)
        dx = math.cos(rad) * self.wys / 2
        dy = math.sin(rad) * self.wys / 2
        return (self.x + dx, self.y + dy)

    def strzel_laser(self, sciany, powierzchnia , kąt):
        
        start = self.get_przod()
        rad = math.radians(self.kat - 90 + kąt)
        dx = math.cos(rad)
        dy = math.sin(rad)

        max_dlugosc = 1000
        
        for i in range(1, max_dlugosc):
            punkt = (start[0] + dx * i, start[1] + dy * i)
            for sciana in sciany:
                if sciana.collidepoint(punkt):
                    #pygame.draw.line(powierzchnia, (255, 0, 0), start, punkt, 2)
                    odleglosc = int(math.hypot(punkt[0] - start[0], punkt[1] - start[1]))
                    if odleglosc - 14 < 1200: 
                        return (odleglosc - 14) /1200
        
        koniec = (start[0] + dx * max_dlugosc, start[1] + dy * max_dlugosc)
        #pygame.draw.line(powierzchnia, (255, 0, 0), start, koniec, 2)
        return 1.0
    def lasery(self, sciany, powierzchnia):
        wspuł = [0 , 45 , 90 ,135 , 180]
        od = []
        for w in wspuł :
            od.append(self.strzel_laser( sciany, powierzchnia, w))
        return od 
            
    def kolizja_awaryjna(self, sciany):
        punkty = self.get_punkty()
        hitbox = pygame.Rect(min(p[0] for p in punkty), min(p[1] for p in punkty),
                             max(p[0] for p in punkty) - min(p[0] for p in punkty),
                             max(p[1] for p in punkty) - min(p[1] for p in punkty))
        punkty = self.get_punkty()
        for sciana in sciany:
            for punkt in punkty:
                if sciana.collidepoint(punkt):
                    return True
    
        return False

    def draw(self, powierzchnia):
        pygame.draw.polygon(powierzchnia, (0, 200, 0), self.get_punkty())
        # Debug: pokaż punkty
        for p in self.get_punkty():
             pygame.draw.circle(powierzchnia, (255, 0, 0), (int(p[0]), int(p[1])), 3)
def load_json(file):
    with open(file, "r", encoding="utf-8") as f: 
        data = json.load(f)    
    return data["map"] , data["check_point"]
class cele :
    def __init__(self , point_cele):
        self.cele = [ pygame.Rect(point[0],point[1], 60, 60) for point in point_cele]
        self.visited = { (rect.x, rect.y): 0 for rect in self.cele }

    def colide_tick(self , czolg):
        reward =  0
        for cel in self.cele :
            if czolg.kolizja([cel]):
                if self.visited[(cel.x, cel.y)] != -1 :
                    self.visited[(cel.x, cel.y)] += 1
                    if self.visited[(cel.x, cel.y)] > 20 :
                        reward -= 1
                    
                elif self.cele.index(cel) == 0 and all(el == -1 for el in self.visited.values()):
                    reward += 100
                    self.new_start()
                else :
                    reward -= 10
            elif not czolg.kolizja([cel]) and  self.visited[(cel.x, cel.y)] > 0 :
                self.visited[(cel.x, cel.y)] = -1
        return reward
    def new_start(self):
        self.visited = { (rect.x, rect.y): 0 for rect in self.cele }



def draw_cele( point_cel ):
    for i , cel in enumerate(point_cel) :
        okno.blit(font.render(f"{i}", True, (255 , 255 , 0)),cel)
        x , y = cel
        pygame.draw.rect(okno, (255 ,0 , 255), (x, y, 60, 60), 3)
class agent():
    def __init__(self , c , genome, config):
        self.czolg = Czolg(390, 500, 31* centymetr, 15* centymetr)
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.cel = cele(c)
        self.reward= 0
    def tick(self , sciany):
        state =self.czolg.lasery( sciany , okno)
        pred = self.net.activate(state)
        action = pred.index(max(pred))
        #faktyczna symulacja 
        tank_collision_with_walls = 0
        kolizja = self.czolg.update(action , sciany)
        if kolizja :
            tank_collision_with_walls -= 25
        self.reward += self.cel.colide_tick(self.czolg) + tank_collision_with_walls
    def draw(self):
        self.czolg.draw(okno)
        
    
        
class env :
    def __init__(self):
        self.s , self.c = load_json("dane.json")
        self.sciany = list_sciana(self.s)

    def plot(self , scores):
        X = [x for x in range(len(scores))]
        """Funkcja do rysowania wykresu wyników na żywo."""
        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.clf()
        plt.title('Training...')
        plt.xlabel('Number of Games')
        plt.ylabel('Score')
        plt.plot(X,scores)
        plt.ylim(ymin=0)
        plt.show(block=False)
        plt.pause(.1)
    def symulacja(self , genomes, config):
        tury = (len(self.c) * 32)* 2
        line_genome = []
        for genome_id, genome in genomes:
            line_genome.append([genome_id, genome , agent(self.c , genome , config)])
        for tura in range(tury):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                with open("best_genome.pkl", "wb") as f: 
                    pickle.dump(line_genome[0][1], f)
                pygame.quit()
                sys.exit()

            for _ ,_  , n in line_genome :
                n.tick(self.sciany)
            
            if keys[pygame.K_1]:
                okno.fill((50, 50, 50))
                for sciana in  self.sciany:
                    sciana.draw(okno)
                for _ ,_ ,a in line_genome :
                    a.draw()
            pygame.display.flip()
        print("new")
        for id , genome , n in line_genome :
            genome.fitness =  n.reward + 0.1
        

a = Word()
winner = a.train()
a.write_genome(winner)
pygame.quit()
