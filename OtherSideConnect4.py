"""
Daria Szabłowska - s24967
Damian Grzesiak - s25866

URUCHOMIENIE:
Aby zainstalować potrzebne biblioteki należy wpisać komendę:
pip install -r requirements.txt

O GRZE:
Connect4 to gra strategiczna dla dwóch graczy,
 którzy na przemian wrzucają swoje żetony do pionowej planszy złożonej z 7 kolumn i 6 rzędów.
 Celem gry jest ułożenie czterech swoich żetonów w jednej linii (pionowo, poziomo lub ukośnie).

ZASADY:
Dwóch graczy: Jeden gra żółtymi (u nas 1), drugi czerwonymi żetonami(u nas 2).
Ruchy: Gracze na zmianę wrzucają po jednym żetonie do wybranej kolumny. Żeton opada na najniższe wolne miejsce w kolumnie.
Zwycięstwo: Wygrywa ten, kto pierwszy ułoży cztery swoje żetony w jednej linii (poziomo, pionowo lub po przekątnej).
Remis: Jeśli plansza zostanie zapełniona, a żaden z graczy nie ułożył czterech żetonów, gra kończy się remisem.

"""

from easyAI import TwoPlayerGame, AI_Player,Human_Player,Negamax

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'
rows = 6
cols = 7

class MyGame(TwoPlayerGame):
    
    def __init__(self, players):
        """Inicjalizacja planszy 6x7, graczy oraz ustawienie obecnego gracza na 1"""
        self.players=players
        self.current_player = 1
        self.board = [[0 for i in range(cols)] for j in range(rows)]

    def possible_moves(self):
        """Funkcja zwracąjaca wszystkie możliwe ruchy czyli liste pozostałych miejsc do zagrania żetonu"""
        move_list = []
        for column in range(cols):
            if self.board[0][column]==0:
                move_list.append(column)
        return move_list
    
    def unmake_move(self, move):
        """Funkcja dzięki której AI ma możliwosc cofniecia ruchu - przyspiesza działanie"""
        col = int(move)
        for row in range(rows):
            if self.board[row][col]!=0:
                self.board[row][col]=0
                break

    def make_move(self, move):
        """Wykonywanie ruchu gracza poprzez wpisanie odpowiednio przypisanego dla niego żetonu (1 lub 2) w odpowiedniej kolumnie - zależnie od gracza wykonuąjcego ruch"""
        col = int(move)
        for row in range(5,-1,-1):
            if self.board[row][col]==0:
                self.board[row][col]=self.current_player
                break

    def is_over(self):
        """Sprawdzanie czy gra powinna sie juz zakończyc. Zwraca wartość true jeśli warunki którejś z metod board_is_full lub check_winner zostaną spełnione"""
        return self.board_is_full() or self.check_winner()
    
    def show(self):
        """Funkcja wypisująca biezaca plansze"""
        print("\n".join([" ".join([str(self.get_player_color(self.board[row][col])) for col in range(cols)]) for row in range(rows)]))
        print()

    def board_is_full(self):
        """Sprawdzanie czy cala tablica zostala juz zapelniona"""
        return all(self.board[0][col] != 0 for col in range(cols))
    
    def check_winner(self):
        """Sprawdzanie wygranej w pionie, poziomie, na skos w prawo lub skos w lewo"""
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col]!=0 and (self.check_direction(row,col,1,0) or
                                                self.check_direction(row,col,0,1) or
                                                self.check_direction(row,col,1,1) or
                                                self.check_direction(row,col,1,-1)):
                    return True
        return False

    def check_direction(self,row,col,d_row,d_col):
        """Sprawdzenie czy od danego punktu na planszy wytępują cztery żetony pod rząd
        
        Keyword arguments:
            row (int): Wiersz początkowy
            col (int): Kolumna początkowa
            d_row (int): Kierunek ruchu w wierszach 
            d_col (int): Kierunek ruchu w kolumnach 
        """
        tokens_in_row = 0
        player=self.board[row][col]
        for i in range(4):
            r,c = row+d_row*i,col+d_col*i
            if 0<=r<6 and 0<=c<7 and self.board[r][c]==player:
                tokens_in_row+=1
            else:
                break
        return tokens_in_row == 4
    
    def scoring(self):
        """Funkcja nadająca punkty za ruch dla AI - do oceny skuteczności ruchu"""
        score = 0
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col]==self.current_player:
                    score+=self.evaluate_position(row,col,1,0)
                    score+=self.evaluate_position(row,col,0,1)
                    score+=self.evaluate_position(row,col,1,1)
                    score+=self.evaluate_position(row,col,1,-1)
        return score
    
    def evaluate_position(self,row,col,d_row,d_col):
        """Wyliczenie ilosci wolnych miejsc od danego żetonu (wg. rzędu, kolumny lub skosu) dla bieżącego gracza 
        na podstawie żetonów rozłożonych na planszy

        Keyword arguments:
            row (int): Wiersz początkowy
            col (int): Kolumna początkowa
            d_row (int): Kierunek ruchu w wierszach 
            d_col (int): Kierunek ruchu w kolumnach 
        """
        score = 0
        tokens_in_row = 0
        empty = 0
        player = self.board[row][col]
        for i in range(4):
            r,c = row+d_row*i,col+d_col*i
            if 0 <= r <rows and 0 <= c <cols:
                if self.board[r][c]==player:
                    tokens_in_row+=1
                elif self.board[r][c]==0:
                    empty+=1
                else:
                    break
            else:
                break

        if tokens_in_row==2 and empty>=2:
            score+=5
        elif tokens_in_row==3 and empty>=1:
            score+=50
        elif tokens_in_row==4:
            score+=100000
        return score
    
    def get_player_color(self, player):
        """Dodanie kolorów do żetonów graczy"""
        if player == 1:
            return f"{YELLOW}{player}{RESET}"
        elif player == 2:
            return f"{RED}{player}{RESET}"
        else:
            return player

    
if __name__ == '__main__':
    human_player=Human_Player("Me")
    ai_algo=Negamax(4)
    game = MyGame([human_player,AI_Player(ai_algo)])
    game.play()
    if game.is_over():
        if  game.current_player==2:
            print(f"{GREEN}Wygrałeś{RESET}")
        elif game.current_player==1:
            print(f"{RED}Wygrał komputer{RESET}")
        else:
            print(f"{YELLOW}Remis{RESET}")