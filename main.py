from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
from svcClassifier import SvcClassifier
from decisionTreeClassifier import DecTreeClassifier

def main():
    # Fetch dataset z UCIML
    banknote_authentication = fetch_ucirepo(id=267)
    
    # Dane jako pandas dataframes
    x = banknote_authentication.data.features
    y = banknote_authentication.data.targets
    
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
    
    # Wizualizacja danych
    print("\nVisualizing Data:")
    sns.pairplot(x.assign(Class=y), hue='Class', diag_kind='kde')
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
