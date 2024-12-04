import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import sklearn.metrics
from sklearn.svm import SVC
file_path = "./data_banknote_authentication.txt"
columns = ['variance','skewness','curtosis','entropy','class']
data = pd.read_csv(file_path, header=None,names=columns)
#print(data.head())
x=data[['variance','skewness','curtosis','entropy']]
y=data['class']
# print("cechy(X):")
# print(x.head())
# print("Klasy (y):")
# print(y.head())
'''
dzielenie danych na treniengowe(70%) testowe(30%) z taką samą powtarzalnością(random_state=42)
'''
X_train,X_test, y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=42)

print(f"Liczba przykładów treningowych: {X_train.shape[0]}")
print(f"Liczba przykładów testowych: {X_test.shape[0]}")
tree_model= DecisionTreeClassifier(random_state=42)
tree_model.fit(X_train,y_train)
y_pred_tree=tree_model.predict(X_test)
tree_accuracy =accuracy_score(y_test,y_pred_tree)
'''DecisionTreeClassifier to model drzewa decyzyjnego.
fit(X_train, y_train) uczy model na danych treningowych.
predict(X_test) przewiduje klasy dla danych testowych.
accuracy_score oblicza dokładność (procent poprawnych przewidywań).'''

svm_model = SVC(kernel='linear',random_state=42)
'''SVC(kernel='linear') tworzy model SVM z prostą liniową granicą decyzji.
'''
svm_model.fit(X_train,y_train)
y_pred_svm=svm_model.predict(X_test)
svm_accuracy =accuracy_score(y_test,y_pred_svm)
print(f"Dokładność drzewa decyzyjnego: {tree_accuracy:.2f}")
print(f"Dokładność SVM: {svm_accuracy:.2f}")
