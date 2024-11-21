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
"""
api_key = os.environ['API_KEY']


class RecommendedMovie:
    @staticmethod
    def pearson_correlation_score(dataset, provided_user, user2):
        if provided_user not in dataset or user2 not in dataset:
            raise ValueError(f"User ({provided_user} lub {user2}) not found in dataset")

        common_movies = {item for item in dataset[provided_user] if item in dataset[user2]}
        if not common_movies:
            return 0

        num_of_common_movies = len(common_movies)

        #sumowanie ocen dla wspólnych filmów
        user1_sum = np.sum([dataset[provided_user][item] for item in common_movies])
        user2_sum = np.sum([dataset[user2][item] for item in common_movies])

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
    if type:
        for user2 in json_data:
            if provided_user != user2:
                score = person_score.pearson_correlation_score(json_data, provided_user, user2)
                print(f"Wynik między {provided_user} a {user2}: {score}")
                if score > best_score:
                    best_score = score
                    best_match = user2
        print("_______________________________________:")
        print(f"Polecane filmy dla {provided_user}:")

        if best_match:
            print(f"Najlepszy wynik z uzytkownikem {best_match} {best_score}")

            provided_user_movies = set(json_data[provided_user].keys())

            # DO USUNIECIA W WERSJI KONCOWEJ - TEST
            # print(f"FILMY PODANEGO USERA: {provided_user_movies}")

            best_user_movies = {
                movie: rating
                for movie, rating in json_data[best_match].items()
                if movie not in provided_user_movies
            }

            # DO USUNIECIA W WERSJI KONCOWEJ - TEST
            # Na ten moment jesli najlepszy wynik sie powtarza to przypisuje tylko jednego usera -
            # DO DODANIA - spisywanie najlepszych filmow z kilku list jesli najlepszy wynik jest do kolku osob
            # print(f"FILMY DOPASOWANEGO USERA: {best_user_movies}")

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
        for user2 in json_data:
            if provided_user != user2:
                score = person_score.pearson_correlation_score(json_data, provided_user, user2)
                print(f"Wynik między {provided_user} a {user2}: {score}")
                if score < worst_score:
                    worst_score = score
                    worst_match = user2
        print("_______________________________________:")
        print(f"Nie polecane filmy dla {provided_user}:")

        if worst_match:
            print(f"Najgorszy wynik z uzytkownikem {worst_match} {worst_score}")

            provided_user_movies = set(json_data[provided_user].keys())

            # DO USUNIECIA W WERSJI KONCOWEJ - TEST
            # print(f"FILMY PODANEGO USERA: {provided_user_movies}")

            worst_user_movies = {
                movie: rating
                for movie, rating in json_data[worst_match].items()
                if movie not in provided_user_movies
            }

            # DO USUNIECIA W WERSJI KONCOWEJ - TEST
            # Na ten moment jesli najlepszy wynik sie powtarza to przypisuje tylko jednego usera -
            # DO DODANIA - spisywanie najlepszych filmow z kilku list jesli najlepszy wynik jest do kolku osob
            # print(f"FILMY DOPASOWANEGO USERA: {best_user_movies}")

            # Sortujemy malejąco i wybieramy 5 najlepszych
            top_movies = sorted(worst_user_movies.items(), key=lambda x: x[1], reverse=True)[:5]

            print("Polecane filmy od użytkownika z najgorszym wynikiem:")
            for movie, rating in top_movies:
                if extra_info:
                    getMovieDetails(movie)
                    print(f": {rating}")
                else:
                    print(f"{movie} - Ocena: {rating}")

        else:
            print("Nie znaleziono użytkownika z którym można by porównać.")


def my_help():
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
    text = """
    Software to recomend movies
    creators:
    Daria Szabłowska
    Damian Grzesiak
    """
    print(text)
    pass


def main():
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
