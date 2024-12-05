"""Autorzy:
Daria Szabłowska s24967
Damian Grzesiak s25886

O projekcie:
Projekt klasyfikuje dane za pomocą dwóch różnych modeli uczenia maszynowego: 
maszyny wektorów nośnych (SVM) i drzewa decyzyjnego. Umożliwia użytkownikowi wybór 
jednego z dwóch zbiorów danych (rozróżniania banknotów oraz zwolnień pracowników), następnie przetwarza te dane, 
trenuje modele, ocenia ich dokładność oraz wizualizuje wyniki. 

ABY URUCHOMIĆ PROGRAM NALEŻY: 
Pobrać pliki znajdujące się na repozytorium (branch LAB4). 
Zainstalować wymagane biblioteki, korzystając z pliku requirements.txt. 
W tym celu używając poniższej komendy w terminalu: pip install -r requirements.txt
"""


from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
from svcClassifier import SvcClassifier
from decisionTreeClassifier import DecTreeClassifier

def load_employee_data(filepath="./Employee.csv"):
    """
    Wczytuje dane z pliku Employee.csv.
    Ostatnia kolumna to etykieta, a pozostałe to cechy.
    """
    data = pd.read_csv(filepath)
    x = data.iloc[:, :-1]  # Wszystkie kolumny poza ostatnią jako cechy
    y = data.iloc[:, -1]   # Ostatnia kolumna jako etykieta
    column_names = x.columns
    enc = preprocessing.OrdinalEncoder() # Inicjalizacja klasy enkodera z sklearn
    x = enc.fit_transform(x) # Przekonwertowanie danych tekstowych (kategorie) na ich odpowiednik wartości int
    x = pd.DataFrame(data=x, columns=column_names)

    return x, y

def load_banknote_data():
    """
    Wczytuje dane z datasetu Banknote Authentication.
    """
    banknote_authentication = fetch_ucirepo(id=267)
    x = banknote_authentication.data.features
    y = banknote_authentication.data.targets
    return x, y

def main():
    """Główna funkcja programu:
        Pozwala użytkownikowi wybrać jeden z dwóch zbiorów danych:
        - Banknote Authentication Dataset.
        - Employee Dataset.
        Trenuje SVM i Drzewo Decyzyjne
        Ocenia wydajność obu modeli
        Wizualizuje dane za pomocą biblioteki Seaborn
        Dokonuje predykcji 
    """
    print("Wybierz dataset do analizy:")
    print("1: Banknote Authentication")
    print("2: Employee Data")
    choice = input("Twój wybór (1/2): ").strip()

    if choice == "1":
        print("\nWybrano: Banknote Authentication Dataset")
        x, y = load_banknote_data()
    elif choice == "2":
        print("\nWybrano: Employee Dataset")
        x, y = load_employee_data()
    else:
        print("Niepoprawny wybór. Kończenie programu.")
        return
    
    # Podział danych na treningowe i testowe
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
    
    # Klasyfikator SVM
    print("\n--- SVM Classifier ---")
    svc_classifier = SvcClassifier(X_train, X_test, y_train, y_test)
    svc_classifier.train()
    svc_classifier.evaluate()

    # Klasyfikator Drzewa Decyzyjnego
    print("\n--- Decision Tree Classifier ---")
    dt_classifier = DecTreeClassifier(X_train, X_test, y_train, y_test)
    dt_classifier.train()
    dt_classifier.evaluate()

    print("\nVisualizing Data:")
    # Wykres liniowy
    sns.lineplot(data=x, x=x.columns[0], y=x.columns[1], hue=y)
    plt.title("Line Plot")
    plt.show()

    # Histogram
    sns.histplot(data=x, x=x.columns[0], hue=y, kde=True)
    plt.title("Histogram")
    plt.show()

    sample_inputs = x.sample(5, random_state=np.random.RandomState())  # 5 randomowych 
    print("\nSample Inputs:")
    print(sample_inputs)

    # Predykcje dla obu modeli
    print("\nSVM Predictions:")
    print(svc_classifier.predict(sample_inputs))

    print("\nDecision Tree Predictions:")
    print(dt_classifier.predict(sample_inputs))

if __name__ == "__main__":
    main()
