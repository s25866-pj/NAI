import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix

class DecTreeClassifier:
    def __init__(self, X_train, X_test, y_train, y_test):
        """
        Inicjalizacja klasyfikatora
        
        X_train
        X_test
        y_train
        y_test
        """

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.decissionTree_clf = DecisionTreeClassifier(random_state=42)
    
    def train(self):
        """Trenuje model SVM na treningowych danych"""
        self.decissionTree_clf.fit(self.X_train, self.y_train)
    
    def evaluate(self):
        """Ocenia model na danych testowych"""

        y_pred_tree = self.decissionTree_clf.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred_tree)
        
        print("\nDecission Tree Classifier Evaluation:")
        print(classification_report(self.y_test, y_pred_tree))
        print("Confusion Matrix:")
        print(confusion_matrix(self.y_test, y_pred_tree))
        print(f"Accuracy: {accuracy:.2f}")
    
    def predict(self, sample_inputs):
        return self.decissionTree_clf.predict(sample_inputs)
