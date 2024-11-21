"""Program do rekomendacji i antyrekomendacji filmów i/lub seriali. 

Daria Szablowska
Damian Grzesiak

Program zawiera kilka funkcji - po wpisaniu odpowiednich komend:

    1. INPUT: Imię Nazwisko - (Bez polskich znaków) wypisuje ocenę dopasowania z innymi użytkownikami i 
    na podstawie najlepszego wyniku wypisuje 5 najlepiej ocenionych filmów przez użytkownika.

    2. INPUT: -h - wypisuje nam dostępne w programie komendy

    3. INPUT: Imię Nazwisko -i - podaje nam polecone filmy na podstawie najlepszego dopasowania oraz podstawowe 
    informacje na temat poleconych filmów

    4. INPUT: Imię Nazwisko -w - podaje NIE polecane filmy, których podana osoba powinna unikać

    5. INPUT: Imię Nazwisko -w-i - wyświetla filmy do unikania z dodatkowymi informacjami

    6. INPUT: info <tytuł> - poda informacje o wybranym filmie

    7. INPUT: -w - wychodzi z programu

    8. INPUT: -i - podaje informacje o programie

ABY URUCHOMIĆ NALEŻY:
Pobrać pliki movie_recommendations.py, data.json oraz requirements.txt.
Zainstalować wymagane biblioteki, korzystając z pliku requirements.txt. W tym celu używając poniższej komendy w terminalu:
pip install -r requirements.txt

Plik requirements.txt zawiera wszystkie potrzebne biblioteki, które są niezbędne do prawidłowego działania programu

Do zmiennej api_key przypisać API KEY podany na mailu
"""

import json
import os
import numpy as np
import requests

"""
Otwórz Run > Edit Configurations.
W sekcji Environment Variables kliknij ....
Dodaj zmienną:
Name: API_KEY
Value:  wartość api key
Teraz zmienna będzie dostępna w Pythonie jako os.getenv("API_KEY").

DRUGA OPCJA: Do zmiennej api_key bezpośrednio wpisać klucz API.
"""
api_key = os.environ['API_KEY']


class RecommendedMovie:

    @staticmethod
    def pearson_correlation_score(dataset, provided_user, user2):
        """Oblicza współczynnik pearsona między dwoma użytkownikami na podstawie ocenionych filmów

        Parametry:
            dataset: Dane użytkowników z ocenami filmów.
            provided_user (str): Użytkownik, dla którego obliczamy podobieństwo.
            user2: Uzytkownik z którym porównujemy oceny.

        Output:
            Wynik w postaci liczby - współczynnik korelacji Pearsona
        """
        #Błąd jeżeli nie ma danego użytkownika w bazie
        if provided_user not in dataset or user2 not in dataset:
            raise ValueError(f"User ({provided_user} lub {user2}) not found in dataset")

        #wspólne filmy ocenione przez użytkowników
        common_movies = {item for item in dataset[provided_user] if item in dataset[user2]}
        if not common_movies:
            return 0

        num_of_common_movies = len(common_movies)

        #sumowanie ocen dla wspólnych filmów
        user1_sum = np.sum([dataset[provided_user][item] for item in common_movies])
        user2_sum = np.sum([dataset[user2][item] for item in common_movies])

        #sumy kwadratów ocen
        user1_squared_sum = np.sum([np.square(dataset[provided_user][item]) for item in common_movies])
        user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in common_movies])

        sum_of_products = np.sum([dataset[provided_user][item] * dataset[user2][item] for item in common_movies])

        Sxy = sum_of_products - (user1_sum * user2_sum / num_of_common_movies)
        Sxx = user1_squared_sum - (user1_sum ** 2) / num_of_common_movies
        Syy = user2_squared_sum - (user2_sum ** 2) / num_of_common_movies

        if Sxx * Syy == 0:
            return 0

        return Sxy / np.sqrt(Sxx * Syy)


def getMovieDetails(film):
    """Funkcja służąca do pobierania informacji o filmie z OMDBAPI
    
    Parametry:
        film: tytuł filmu

    Output:
        Zwraca informacje o filmie
    """

    base_url = "https://www.omdbapi.com/"
    params = {
        "t": film,  # Tytuł filmu
        "apikey": api_key  # Twój klucz API
    }
    try:
        # Wysyłanie żądania do API
        response = requests.get(base_url, params=params)
        # Sprawdzenie statusu HTTP
        if response.status_code == 200:
            data = response.json()  # Parsowanie odpowiedzi do formatu JSON

            # Sprawdzenie, czy API zwraca dane
            if data.get("Response") == "True":
                #print("Pełna odpowiedź z API:")
                print("Tytuł: " + data["Title"])
                print("Czas Trwania: " + data["Runtime"])
                print("opis (język ang): " + data["Plot"])
                # print(data)  # Wyświetlenie pełnej odpowiedzi
                return data
            else:
                print(f"Błąd API: {data.get('Error', 'Nieznany błąd')}")
                return None
        else:
            print(f"Błąd: Nie udało się połączyć z API. Status HTTP: {response.status_code}")
            return None
    except Exception as e:
        print(f"Wyjątek podczas wysyłania żądania: {e}")
        return None


def searchRecommendation(provided_user, extra_info, type):
    """ Funkcja wyszukuje rekomendacje i anty-rekomendacje filmów dla podanego użytkownika na 
    podstawie podobieństwa jego ocen z innymi użytkownikami.
    
    Parametry:
        provided_user - wprowadzony użytkownik dla którego mają zostać polecone filmy
        extra_info - wypisanie dodatkowych informacji jeśli wartość bool będzie TRUE
        type - jeśli będzie true to wyszukuje najlepsze dopasowania, jak false to najgorsze"""
    
    ratings_file = './data.json'
    print("osoba")
    with open(ratings_file, 'r') as f:
        json_data = json.load(f)

    person_score = RecommendedMovie()


    best_match = None
    best_score = -1
    worst_match = None
    worst_score = 1
    recomended_user_movies = []
    
    best_match = None
    best_score = -1
    worst_match = None
    worst_score = 1
    recomended_user_movies = []
    if type:
        #Wywołanie metody zwracającej najlepszy wynik i najlepsze dopasowanie
        best_score, best_match = find_best_match(json_data, provided_user, person_score)

        print("_______________________________________:")
        print(f"Polecane filmy dla {provided_user}:")

        if best_match:
            print(f"Najlepszy wynik z uzytkownikem {best_match} {best_score}")
            # Filmy, które są ocenione przez najlepszego użytkownika, ale nie wypisane przez podanego użytkownika
            provided_user_movies = set(json_data[provided_user].keys())

            best_user_movies = {
                movie: rating
                for movie, rating in json_data[best_match].items()
                if movie not in provided_user_movies
            }

            # Sortujemy malejąco i wybieramy 5 najlepszych
            top_movies = sorted(best_user_movies.items(), key=lambda x: x[1], reverse=True)[:5]

            print("Polecane filmy od użytkownika z najlepszym wynikiem:")
            for movie, rating in top_movies:
                if extra_info:
                    getMovieDetails(movie)
                    print(f": {rating}")
                else:
                    print(f"{movie} - Ocena: {rating}")

        else:
            print("Nie znaleziono użytkownika z którym można by porównać.")
    else:
        #Wywołanie metody zwracającej najlepszy wynik i najlepsze dopasowanie
        best_score, best_match = find_best_match(json_data, provided_user, person_score)

        print("_______________________________________:")
        print(f"Nie polecane filmy dla {provided_user}:")

        if best_match:
            print(f"Najlepszy wynik z uzytkownikem {best_match} {best_score}")

            #Także pomijamy filmy ocenione przez użytkownika, których nie ogladal podany użytkownik
            provided_user_movies = set(json_data[provided_user].keys())
            worst_user_movies = {
                movie: rating
                # for movie, rating in json_data[worst_match].items()
                for movie, rating in json_data[best_match].items()
                if movie not in provided_user_movies
            }
            # Sortujemy rosnąco i wybieramy 5 pierwszych - najgorszych wyników
            top_movies = sorted(worst_user_movies.items(), key=lambda x: x[1], reverse=False)[:5]
            print("Filmy których powinieneś unikać:")
            for movie, rating in top_movies:
                if extra_info:
                    getMovieDetails(movie)
                    print(f": {rating}")
                else:
                    print(f"{movie} - Ocena: {rating}")
        else:
            print("Nie znaleziono użytkownika z którym można by porównać.")

def find_best_match(json_data, provided_user, person_score):
    """"Metoda obliczająca najlepsze dopasowanie pomiędzy osobami (Pearson Score) wykorzystując metodę pearson_correlation_score. Metoda przechodzi przez 
    cały dataset osób i dla każdego elementu oblicza Pearson score, zapisując i zwracając najlepsze dopasowanie."""

    best_match = None
    best_score = -1

    for user2 in json_data:
        if provided_user != user2:
            score = person_score.pearson_correlation_score(json_data, provided_user, user2)
            print(f"Wynik między {provided_user} a {user2}: {score}")
            if score > best_score:
                best_score = score
                best_match = user2
    
    return best_score, best_match


def my_help():
    """Wyświetla pomoc dot. komend uzywanych w programie"""

    text = """
    name sname -i : information about a recomended movie
    name sname -w : worst recomended movie
    name sname -w-i :information about a worst recomended movie
    info <title> : information about movie
    -i : information about program creation
    -w : exit from program
    """
    print(text)
    pass


def information():
    """Wyświetla informacje o programie"""

    text = """
    Software to recomend movies
    creators:
    Daria Szabłowska
    Damian Grzesiak
    """
    print(text)
    pass


def main():
    """Główna funkcja obsługująca wybór odpowiednich komend"""

    while True:
        provided_user = input(
            "Podaj osobę dla ktorej chcesz otrzymac listę poleconych filmow (imie i nazwisko BEZ POLSKICH ZNAKOW) lub info <tytuł>: ")
        if provided_user[0] == "-":
            if provided_user[1] == "h":
                my_help()
            elif provided_user[1] == "i":
                information()
            elif provided_user[1] == "w":
                print("Dziękujemy za skorzystanie z programu.")
                break
            else:
                print('brak komendy, po pomoc wpisz "-h".')
        else:
            if provided_user.lower().startswith("info") and "<" in provided_user and ">" in provided_user:
                start = provided_user.find("<") + 1  # Znajdź pozycję znaku "<" i przesuwamy o 1
                end = provided_user.find(">", start)  # Znajdź pierwsze ">" po "<"
                film = provided_user[start:end]  # Wyciągamy tekst pomiędzy "<" i ">"
                getMovieDetails(film)
            elif len(provided_user.split()) == 2 and all(
                    part.isalpha() and part[0].isupper() for part in provided_user.split()):
                searchRecommendation(provided_user, False, True)
            elif provided_user[-2:] == "-i" and provided_user[-4:-2] != "-w":
                provided_user = provided_user[:-3]
                searchRecommendation(provided_user, True, True)
            elif provided_user[-2:] == "-w":
                provided_user = provided_user[:-3]
                searchRecommendation(provided_user, False, False)
            elif provided_user[-2:] == "-i" and provided_user[-4:-2] == "-w":
                provided_user = provided_user[:-5]
                print(provided_user)
                searchRecommendation(provided_user, True, False)


if __name__ == '__main__':
    main()
