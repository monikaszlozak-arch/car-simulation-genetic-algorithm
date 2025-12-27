import pygame
import sys
import random
import time
import precise_editing as pe
import json
pygame.init()
okno = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Obrócone prostokąty")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
font_kordy = pygame.font.SysFont(None, 20)
tk_ctve = pe.change_the_values_exactly()
tk_instruction = pe.instruction()
def siatka():
    for x in range(0 , 800 ,30):
        okno.blit(font.render(f"({x} \n,{0})", True, (255 , 255 , 255)),(x ,0))
        for y in range(0,600,30) :
            okno.blit(font.render(f"({0} \n,{y})", True, (255 , 255 , 255)),(0 ,y))
            pygame.draw.line(okno ,(0, 255, 0), (x ,y), (x , 600), 2)
            pygame.draw.line(okno ,(0, 255, 0), (x ,y), (800 , y), 2)
def kordy(x , y , sy , sx ,r ):
    okno.blit(font_kordy.render(f"{x}", True, (255 , 255 , 255)),(0 ,0))
    okno.blit(font_kordy.render(f"{y}", True, (255 , 255 , 255)),(0 ,30))
    okno.blit(font_kordy.render(f"{sx}", True, (255 , 255 , 255)),(0 ,60))
    okno.blit(font_kordy.render(f"{sy}", True, (255 , 255 , 255)),(0 ,90))
    okno.blit(font_kordy.render(f"{r}", True, (255 , 255 , 255)),(0 ,120))

def wyswietl_nagrody(nl):
    for i , n in enumerate(nl):
        okno.blit(font.render(f"{i}", True, (255 , 255 , 0)),n)
        x , y =n
        pygame.draw.rect(okno, (255 ,0 , 255), (x, y, 60, 60), 3)

def write_json(mapa , check_point):
    dane = {"map" : mapa,   "check_point": check_point}
    with open("dane.json", "w", encoding="utf-8") as plik:
        json.dump(dane, plik, ensure_ascii=False, indent=4)
# Lista obiektów: (obraz, prostokat)
def main():
    blocking = False
    prostokaty = []
    tor = []
    nagrody = []
    # Parametry prostokąta
    centymetr = 1
    szerokosc = 60
    wysokosc = 40
    kolor = (0, 200, 255)

    dziala = True
    rotation = 0
    real_rotation = 0
    czy_siatka = 0
    while dziala:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dziala = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    prostokaty.append((obrocona, prostokat))
                    tor.append(dane)
                    print(tor)
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_1: 
                    if czy_siatka == 0:
                        czy_siatka = 1
                    elif czy_siatka == 1:
                        czy_siatka = 0
                if event.key == pygame.K_2: 
                        x, y = pygame.mouse.get_pos()
                        nagrody.append((x,y))
                        print(nagrody)
                if event.key == pygame.K_3: 
                    if blocking == False :
                        blocking = True    
                    elif blocking == True :
                        blocking = False  
                if event.key == pygame.K_4 and blocking == True: 
                    prostokaty.append((obrocona, prostokat))
                    tor.append(dane)
                    blocking = False
                if event.key == pygame.K_6:
                    prostokaty.remove(prostokaty[-1])   
                if event.key == pygame.K_7:
                    write_json(tor , nagrody) 
                if event.key == pygame.K_8: 
                    nagrody.remove(nagrody[-1])
                    
        if blocking == False :
            
            x, y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        
        # ustawiamy według klawiszy
        if keys[pygame.K_a]:
            rotation += 1
            real_rotation -= 1                
        if keys[pygame.K_s]:                    
            rotation -= 1
            real_rotation += 1 
        if keys[pygame.K_q]:
            szerokosc += 1                    
        if keys[pygame.K_w]:                    
            szerokosc -= 1
        if keys[pygame.K_e]:
            wysokosc+= 1                    
        if keys[pygame.K_d]:                    
            wysokosc -= 1
        
                             
            
                          
         

        # ustawiamy według tk 
        ustawienia = tk_ctve.update()
        real_rotation = ustawienia[0]
        rotation = -ustawienia[0]
        szerokosc = ustawienia[1]
        wysokosc = ustawienia[2]
        if  keys[pygame.K_5]: # potwierdzenie (ułatwenie dla mnie bo nie chciało mi się tego programować versja 3 mam już to mieć )   
            x += ustawienia[3]
            y += ustawienia[4]



        dane = [x,y , szerokosc , wysokosc , real_rotation]     
        powierzchnia = pygame.Surface((szerokosc* centymetr, wysokosc* centymetr), pygame.SRCALPHA)
        pygame.draw.rect(powierzchnia, kolor, (0, 0, szerokosc * centymetr, wysokosc* centymetr))

                        # Obracamy powierzchnię
        obrocona = pygame.transform.rotate(powierzchnia, rotation)
        prostokat = obrocona.get_rect(center=(x, y))
        okno.fill((30, 30, 30))
        if czy_siatka == 1 :
                siatka()
        kordy(x,y , szerokosc , wysokosc , real_rotation)
        okno.blit(obrocona, prostokat)
        for obraz, prostokatt in prostokaty:
            okno.blit(obraz, prostokatt)
        
        #gracz
        pygame.draw.rect(okno, (255 , 0 ,0), pygame.rect.Rect(390, 500, 31 * centymetr, 15* centymetr))
        wyswietl_nagrody(nagrody)
        pygame.display.update()
        pygame.display.flip()
        tk_instruction.update()
        clock.tick(60)
        
        
main()
pygame.quit()
sys.exit()
