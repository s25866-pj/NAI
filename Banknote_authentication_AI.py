import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import classification_report
from tensorflow.keras.optimizers import Adam

def read_CSV(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    data = [line.strip().split(",") for line in lines]
    return pd.DataFrame(data, columns=["F1", "F2", "F3", "F3", "result"]).astype(float)

file_path = "data_banknote_authentication.txt"
try:
    data = read_CSV(file_path)
except FileNotFoundError:
    print(f"File {file_path} not found. Please provide a valid path.")
    exit()

print(data)
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)  # poprawka na transformowanie, a nie dopasowywanie

model = Sequential([
    Dense(16, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(8, activation='relu'),
    Dense(1,activation='sigmoid')
])
model.compile(optimizer=Adam(learning_rate=0.01),loss='binary_crossentropy',metrics=['accuracy'])
history=model.fit(X_train, y_train, epochs=50,batch_size=4, validation_split=0.2,verbose=2)
loss, accuracy = model.evaluate(X_test, y_test,verbose=0)
print(f"Loss: {loss}, Accuracy: {accuracy}")

predictions = (model.predict(X_test)>0.5).astype(int)

print("\nClassification Report:\n")
print(classification_report(y_test, predictions))
