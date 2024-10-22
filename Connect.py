from tabnanny import check
import random
import time
import numpy as np

from easyAI import TwoPlayerGame

wiersze = 6
kolumny=7
playerturn=True
endGame=False
tablica = [[0 for _ in range(kolumny)] for _ in range(wiersze)]

class ConnectGame(TwoPlayerGame):
    
    def __init__(self, players):
        self.players = players
        self.current_player = 1

    def possible_moves(self):
        return

    def make_move(self, move):
        return
    
    def show(self):
        return 

    def lose(self):
        return checkGame(self.opponent) != 0
        
    def is_over(self):
        return
        

def showGame():
    for wiersz in tablica:
        print(wiersz)
    print("\n")
    
def isFull(kolumna):
    if((tablica[0][kolumna])>0):
        return True
    else:
        return False
    
def addToken(kolumna, gracz):
    for wiersz in range(wiersze -1, -1, -1):
        if tablica[wiersz][kolumna] == 0:
            tablica[wiersz][kolumna] = gracz
            break
      
def playerMove():
    while True:
        kolumna = int(input("Podaj kolumne od 1 do 7: "))  - 1
        if 0 <= kolumna < kolumny and not isFull(kolumna):
            addToken(kolumna, 1)
            break
        else:
            print("Nie mozna dodac zetonu w tym miejscu")

def aiMove():
    while True:
        kolumna = random.randint(0, kolumny - 1)
        if not isFull(kolumna):
            addToken(kolumna, 2)
            print(f"Przeciwnik dodal zeton w kolumnie: {kolumna + 1}")
            break
            
def checkGame(gracz):
    global endGame
    #zwyciestwo pion
    for kolumna in range(kolumny):
        for wiersz in range(wiersze - 3):  
            gracz = tablica[wiersz][kolumna]
            if gracz != 0:
                if (tablica[wiersz + 1][kolumna] == gracz and
                    tablica[wiersz + 2][kolumna] == gracz and
                    tablica[wiersz + 3][kolumna] == gracz):
                    endGame = True
                    return gracz  
    #zwyciestwo poziom
    for wiersz in range(wiersze):
        for kolumna in range(kolumny - 3): 
            gracz = tablica[wiersz][kolumna]
            if gracz != 0:
                if (tablica[wiersz][kolumna + 1] == gracz and
                    tablica[wiersz][kolumna + 2] == gracz and
                    tablica[wiersz][kolumna + 3] == gracz):
                    endGame = True
                    return gracz  
    
    #zwyciestwo skos prawo
    for kolumna in range(kolumny - 3):
        for wiersz in range(3, wiersze):  
            gracz = tablica[wiersz][kolumna]
            if gracz != 0:
                if (tablica[wiersz - 1][kolumna + 1] == gracz and
                    tablica[wiersz - 2][kolumna + 2] == gracz and
                    tablica[wiersz - 3][kolumna + 3] == gracz):
                    endGame = True
                    return gracz  

    return 0

# showGame()
# while not endGame:
#     if playerturn:
#         playerMove()
#         print("PLANSZA PO TWOIM RUCHU")
#         winner = checkGame()
#     else:
#         print("PLANSZA PO RUCHU PRZECIWNIKA")
#         time.sleep(1)
#         aiMove()
#         winner = checkGame()
    
#     if winner != 0:
#         endGame = True
#         print(f"Wygrał gracz {winner}")
    
#     playerturn = not playerturn
#     showGame()

if __name__ == '__main__':

    from easyAI import Human_Player, AI_Player, Negamax

    human_player = Human_Player("Me")
    ai_negamax = Negamax(4)

    game = ConnectGame([Human_Player(human_player), AI_Player(ai_negamax)])
    game.play()

    if game.lose():
        print(f"Wygral gracz {game.opponent}")