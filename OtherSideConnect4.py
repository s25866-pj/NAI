from easyAI import TwoPlayerGame, AI_Player,Human_Player,Negamax
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'
rows = 6
cols = 7
class MyGame(TwoPlayerGame):
    def __init__(self, players):
        self.players=players
        self.current_player = 1
        self.board = [[0 for i in range(cols)] for j in range(rows)]
    def possible_moves(self):
        move_list = []
        for column in range(cols):
            if self.board[0][column]==0:
                move_list.append(column)
        return move_list
    def unmake_move(self, move):
        col = int(move)
        for row in range(rows):
            if self.board[row][col]!=0:
                self.board[row][col]=0
                break
    def make_move(self, move):
        col = int(move)
        for row in range(5,-1,-1):
            if self.board[row][col]==0:
                self.board[row][col]=self.current_player
                break
    def is_over(self):
        return self.board_is_full() or self.check_winner()
    def show(self):
        print("\n".join([" ".join([str(self.board[row][col]) for col in range(cols)]) for row in range(rows)]))
        print()
    def board_is_full(self):
        return all(self.board[0][col] != 0 for col in range(cols))
    def check_winner(self):
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col]!=0 and (self.check_direction(row,col,1,0) or
                                                self.check_direction(row,col,0,1) or
                                                self.check_direction(row,col,1,1) or
                                                self.check_direction(row,col,1,-1)):
                    return True
        return False

    def check_direction(self,row,col,d_row,d_col):
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
            score+=10
        elif tokens_in_row==3 and empty>=1:
            score+=100
        elif tokens_in_row==4:
            score+=10000
        return score
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