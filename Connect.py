from tabnanny import check
wiersze = 6
kolumny=7
playerturn=True
endGame=False
tablica = [[0 for _ in range(kolumny)] for _ in range(wiersze)]
def showGame():
    for wiersz in tablica:
        print(wiersz)
    print("\n")
def isFull(kolumna):
    if((tablica[0][kolumna])>0):
        return True
    else:
        return False
def addToken():
    kolumna = int(input("Podaj kolumne do której cesz dodać rzeton"))
    if playerturn:
        gracz=1
    else:
        gracz=2
    if isFull(kolumna):
        print("Nie możesz dodać tokenu")

    else:
        for wiersz in range(wiersze - 1, -1, -1):
            if tablica[wiersz][kolumna] == 0:
                tablica[wiersz][kolumna] = gracz
                break
def checkGame():
    global endGame
    for wiersz in range(wiersze-4):
        for kolumna in range(kolumny-3):
            gracz=tablica[wiersz][kolumna]
            if gracz==0:
                continue
            if(tablica[wiersz+1][kolumna]==gracz and tablica[wiersz+2][kolumna]==gracz and tablica[wiersz+3][kolumna]==gracz ):
                endGame=False
            elif(tablica[wiersz+1][kolumna+1]==gracz and tablica[wiersz+2][kolumna+2]==gracz and tablica[wiersz+3][kolumna+3]==gracz):
                endGame= False
            elif(tablica[wiersz][kolumna+1]==gracz and tablica[wiersz][kolumna+2]==gracz and tablica[wiersz][kolumna+3]==gracz):
                endGame= False
            else : endGame= True


showGame()
while not endGame:
    if playerturn:
        addToken()
        checkGame()
    else:
        addToken()
        checkGame()
    playerturn=not playerturn
    showGame()
if playerturn:
    print("gratuluję,wygrałeś")
else:
    print("wygrał komputer")