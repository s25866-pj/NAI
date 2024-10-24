import numpy as np
import sys
#TODO Pełna dokumentacja
from easyAI import TwoPlayerGame

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'
rows = 6
columns = 7
playerturn = True
endGame = False
board = [[0 for _ in range(columns)] for _ in range(rows)]

class ConnectGame(TwoPlayerGame):
    #Tisuje tylko po to żeby wymusić aktualizcje
    
    def __init__(self, players):
        self.players = players
        self.current_player = 1
    def possible_moves(self):
        # TODO Sprawdzić w naszej tablicy, czy dla danej kolumny możena wstawić żeton. Obecny for działa źle.
        freeColumns = []
        for column in range(columns):
            if(board[0][column])== 0:
                freeColumns.append(column)
        print(freeColumns)
        return freeColumns
    def make_move(self, column):
        #TODO Wykonanie akcji zagrania żetona (może działa)
        for row in range(rows - 1, -1, -1):
            if board[row][column] == 0:
                board[row][column] = self.current_player
                break
        # line = np.argmin(tablica[:, column] != 0)
        # tablica[line, column] = self.player
    
    def show(self):
        showGame() 

    def lose(self):
        return get_winner(self.opponent) != 0
        
    def is_over(self):
        return is_draw() or self.lose()
    
    def scoring(self):
        return -100 if self.lose() else 0
        

def showGame():
    for row in board:
        print(row)
    print("\n")

def get_winner(player):

     # Sprawdzanie pionowe
    for row in range(rows - 3):
        for kolumna in range(columns):
            player = board[row][kolumna]
            if player != 0 and all(board[row + i][kolumna] == player for i in range(4)):
                return player

    # Sprawdzanie poziome
    for row in range(rows):
        for kolumna in range(columns - 3):
            player = board[row][kolumna]
            if player != 0 and all(board[row][kolumna + i] == player for i in range(4)):
                return player

    # Sprawdzanie ukośne (z lewej do prawej, w dół)
    for row in range(rows - 3):
        for kolumna in range(columns - 3):
            player = board[row][kolumna]
            if player != 0 and all(board[row + i][kolumna + i] == player for i in range(4)):
                return player

    # Sprawdzanie ukośne (z prawej do lewej, w dół)
    for row in range(rows - 3):
        for kolumna in range(3, columns):
            player = board[row][kolumna]
            if player != 0 and all(board[row + i][kolumna - i] == player for i in range(4)):
                return player
    
    return 0

def is_draw():
    zeros = sum(board[wiersz][kolumna] == 0 for wiersz in range(rows) for kolumna in range(columns))
    if zeros == 0:
        print(f"{YELLOW}Remis{RESET}")
        return True
    
    return False

if __name__ == '__main__':

    from easyAI import Human_Player, AI_Player, Negamax

    human_player = Human_Player("Me")
    ai_negamax = Negamax(4)

    game = ConnectGame([Human_Player(human_player), AI_Player(ai_negamax)])
    game.play()

    if game.lose():
        print(f"Wygral gracz {game.opponent_index}")

