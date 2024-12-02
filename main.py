from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
from ucimlrepo import fetch_ucirepo
from banknoteClassifier import BanknoteClassifier

def main():
    # Fetch dataset z UCIML
    banknote_authentication = fetch_ucirepo(id=267)
    
    # Dane jako pandas dataframes
    X = banknote_authentication.data.features
    y = banknote_authentication.data.targets
    
    # Podział danych na treningowe i testowe
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    classifier = BanknoteClassifier(X_train, X_test, y_train, y_test)
    classifier.train()
    classifier.evaluate()
    
    # Wizualizacja danych
    print("\nVisualizing Data:")
    sns.pairplot(X.assign(Class=y), hue='Class', diag_kind='kde')
    plt.show()
    
    sample_inputs = X.sample(5, random_state=42)  # 5 randomowych 
    print("\nSample Inputs:")
    print(sample_inputs)
    print("\nSVM Predictions:")
    print(classifier.predict(sample_inputs))

if __name__ == "__main__":
    main()
