import numpy as np
import sys

from easyAI import TwoPlayerGame

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'
wiersze = 6
kolumny = 7
playerturn = True
endGame = False
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
    return tablica[0][kolumna] > 0

def addToken():
    while True:
        try:
            kolumna = int(input("Podaj kolumnę, do której chcesz dodać żeton: "))
        except ValueError:
            print("Niepoprawny numer kolumny, spróbuj ponownie.")
            continue

        if 0 <= kolumna < kolumny:
            if playerturn:
                gracz = 1
            else:
                gracz = 2

            if isFull(kolumna):
                print("Nie możesz dodać tokenu, kolumna jest pełna.")
            else:
                for wiersz in range(wiersze - 1, -1, -1):
                    if tablica[wiersz][kolumna] == 0:
                        tablica[wiersz][kolumna] = gracz
                        return
        else:
            print("Niepoprawny numer kolumny, spróbuj ponownie.")

def checkGame(gracz):
    global endGame

    # Sprawdzanie pionowe
    for wiersz in range(wiersze - 3):
        for kolumna in range(kolumny):
            gracz = tablica[wiersz][kolumna]
            if gracz != 0 and all(tablica[wiersz + i][kolumna] == gracz for i in range(4)):
                endGame = True
                return gracz

    # Sprawdzanie poziome
    for wiersz in range(wiersze):
        for kolumna in range(kolumny - 3):
            gracz = tablica[wiersz][kolumna]
            if gracz != 0 and all(tablica[wiersz][kolumna + i] == gracz for i in range(4)):
                endGame = True
                return gracz

    # Sprawdzanie ukośne (z lewej do prawej, w dół)
    for wiersz in range(wiersze - 3):
        for kolumna in range(kolumny - 3):
            gracz = tablica[wiersz][kolumna]
            if gracz != 0 and all(tablica[wiersz + i][kolumna + i] == gracz for i in range(4)):
                endGame = True
                return gracz

    # Sprawdzanie ukośne (z prawej do lewej, w dół)
    for wiersz in range(wiersze - 3):
        for kolumna in range(3, kolumny):
            gracz = tablica[wiersz][kolumna]
            if gracz != 0 and all(tablica[wiersz + i][kolumna - i] == gracz for i in range(4)):
                endGame = True
                return gracz

    # Sprawdzenie, czy nie ma więcej miejsca na planszy (remis)
    zeros = sum(tablica[wiersz][kolumna] == 0 for wiersz in range(wiersze) for kolumna in range(kolumny))
    if zeros == 0:
        print(f"{YELLOW}Remis{RESET}")
        sys.exit(0)

# showGame()

# while not endGame:
#     if playerturn:
#         addToken()
#         checkGame()
#     else:
#         addToken()
#         checkGame()
#     playerturn=not playerturn
#     showGame()
# if playerturn:
#     print(f"{GREEN}Gratulacje, wygrałeś!{RESET}")
# else:
#     print(f"{RED}Wygrał komputer{RESET}")

if __name__ == '__main__':

    from easyAI import Human_Player, AI_Player, Negamax

    human_player = Human_Player("Me")
    ai_negamax = Negamax(4)

    game = ConnectGame([Human_Player(human_player), AI_Player(ai_negamax)])
    game.play()

    if game.lose():
        print(f"Wygral gracz {game.opponent}")

