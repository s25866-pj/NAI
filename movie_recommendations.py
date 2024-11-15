import json
import numpy as np


class RecommendedMovie:
    @staticmethod
    def pearson_correlation_score(dataset, user1, user2):
        if user1 not in dataset or user2 not in dataset:
            raise ValueError(f"User ({user1} lub {user2}) not found in dataset")

        common_movies = {item for item in dataset[user1] if item in dataset[user2]}
        if not common_movies:
            return 0
        
        num_of_common_movies = len(common_movies)

        #sumowanie ocen dla wspólnych filmów
        user1_sum = np.sum([dataset[user1][item] for item in common_movies])
        user2_sum = np.sum([dataset[user2][item] for item in common_movies])

        user1_squared_sum = np.sum([np.square(dataset[user1][item]) for item in common_movies])
        user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in common_movies])

        sum_of_products = np.sum([dataset[user1][item] * dataset[user2][item] for item in common_movies])

        Sxy = sum_of_products - (user1_sum * user2_sum / num_of_common_movies)
        Sxx = user1_squared_sum - (user1_sum ** 2) / num_of_common_movies
        Syy = user2_squared_sum - (user2_sum ** 2) / num_of_common_movies


        if Sxx * Syy == 0:
            return 0

        return Sxy / np.sqrt(Sxx * Syy)


def main():
    ratings_file = 'data.json'

    user1 = input("Podaj pierwszego użytkownika: ")
    user2 = input("Podaj drugiego użytkownika: ")

    with open(ratings_file, 'r') as f:
        json_data = json.load(f)

    person_score = RecommendedMovie()
    score = person_score.pearson_correlation_score(json_data, user1, user2)
    print(f"Wynik między {user1} a {user2}: {score}")


if __name__ == '__main__':
    main()
