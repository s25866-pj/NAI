from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

class SvcClassifier:
    def __init__(self, X_train, X_test, y_train, y_test):
        """
        Inicjalizacja klasyfikatora
        
        Parametry:
            X_train - cechy dla danych treningowych
            X_test - ceychy dla danych testowych
            y_train - etykiety (wyniki) dla danych treningowych
            y_test - etykiety (wyniki) dla danych testowych
        """

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.svm_clf = SVC(kernel='linear', random_state=42)
    
    def train(self):
        """Trenuje model SVM na danych treningowych z pomocą metody fit, która pobiera dane wejściowe i dostosowuje parametry modelu, aby nauczyć się wzorców"""
        self.svm_clf.fit(self.X_train, self.y_train)
    
    def evaluate(self):
        """Ocenia model na danych testowych. Robimy predykcje na zbiorze testowym, po czym wyświetlamy raport klasyfikacji oraz macierz pomyłek"""
        y_pred_svm = self.svm_clf.predict(self.X_test)
        
        print("\nSVM Classifier Evaluation:")
        print(classification_report(self.y_test, y_pred_svm))
        print("Confusion Matrix:")
        print(confusion_matrix(self.y_test, y_pred_svm))
    
    def predict(self, sample_inputs):
        """Dokonuje predykcji dla przykładowych danych wejściowych"""
        return self.svm_clf.predict(sample_inputs)
