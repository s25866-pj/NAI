import sys
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'
wiersze = 6
kolumny = 7
playerturn = True
endGame = False
tablica = [[0 for _ in range(kolumny)] for _ in range(wiersze)]

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

def checkGame():
    global endGame

    # Sprawdzanie pionowe
    for wiersz in range(wiersze - 3):
        for kolumna in range(kolumny):
            gracz = tablica[wiersz][kolumna]
            if gracz != 0 and all(tablica[wiersz + i][kolumna] == gracz for i in range(4)):
                endGame = True
                return

    # Sprawdzanie poziome
    for wiersz in range(wiersze):
        for kolumna in range(kolumny - 3):
            gracz = tablica[wiersz][kolumna]
            if gracz != 0 and all(tablica[wiersz][kolumna + i] == gracz for i in range(4)):
                endGame = True
                return

    # Sprawdzanie ukośne (z lewej do prawej, w dół)
    for wiersz in range(wiersze - 3):
        for kolumna in range(kolumny - 3):
            gracz = tablica[wiersz][kolumna]
            if gracz != 0 and all(tablica[wiersz + i][kolumna + i] == gracz for i in range(4)):
                endGame = True
                return

    # Sprawdzanie ukośne (z prawej do lewej, w dół)
    for wiersz in range(wiersze - 3):
        for kolumna in range(3, kolumny):
            gracz = tablica[wiersz][kolumna]
            if gracz != 0 and all(tablica[wiersz + i][kolumna - i] == gracz for i in range(4)):
                endGame = True
                return

    # Sprawdzenie, czy nie ma więcej miejsca na planszy (remis)
    zeros = sum(tablica[wiersz][kolumna] == 0 for wiersz in range(wiersze) for kolumna in range(kolumny))
    if zeros == 0:
        print(f"{YELLOW}Remis{RESET}")
        sys.exit(0)

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
    print(f"{GREEN}Gratulacje, wygrałeś!{RESET}")
else:
    print(f"{RED}Wygrał komputer{RESET}")
