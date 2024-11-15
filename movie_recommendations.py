import json
import numpy as np


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


def main():
    ratings_file = 'data.json'

    provided_user = input("Podaj osobę dla ktorej chcesz otrzymac listę poleconych filmow (imie i nazwisko BEZ POLSKICH ZNAKOW): ")

    with open(ratings_file, 'r') as f:
        json_data = json.load(f)

    person_score = RecommendedMovie()

    best_match = None
    best_score = -1
    recomended_user_movies = []
    

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

        #DO USUNIECIA W WERSJI KONCOWEJ - TEST
        #print(f"FILMY PODANEGO USERA: {provided_user_movies}")

        best_user_movies = {
            movie: rating
            for movie, rating in json_data[best_match].items()
            if movie not in provided_user_movies
        }

        #DO USUNIECIA W WERSJI KONCOWEJ - TEST
        #Na ten moment jesli najlepszy wynik sie powtarza to przypisuje tylko jednego usera - 
        # DO DODANIA - spisywanie najlepszych filmow z kilku list jesli najlepszy wynik jest do kolku osob
        #print(f"FILMY DOPASOWANEGO USERA: {best_user_movies}")

        # Sortujemy malejąco i wybieramy 5 najlepszych
        top_movies = sorted(best_user_movies.items(), key=lambda x: x[1], reverse=True)[:5]

        print("Polecane filmy od użytkownika z najlepszym wynikiem:")
        for movie, rating in top_movies:
            print(f"{movie} - Ocena: {rating}")
    else:
        print("Nie znaleziono użytkownika z którym można by porównać.")

    

if __name__ == '__main__':
    main()
