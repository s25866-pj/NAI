import tensorflow as tf
import matplotlib.pyplot as plt
from keras import datasets, layers, models
from keras import preprocessing
import numpy as np

"""
Autorzy:
Daria Szabłowska s24967
Damian Grzesiak s25866

Aby uruchomić program należy:
Zainstalować wymagane biblioteki, korzystając z pliku requirements.txt.
W tym celu używając poniższej komendy w terminalu: pip install -r requirements.txt

W projekcie używany jest dataset CIFAR10, na podstawie którego uczymy odróżniać obiekty na zdjęciach.
"""

# Ładowanie datasetu CIFAR10
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# Normalizacja wartości do 0 i 1
train_images, test_images = train_images / 255.0, test_images / 255.0

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# Wizualizacja 25 przykładowych obrazów z etykietami klas
plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
# Wyłączenie osi i siatki
    plt.xticks([]), plt.yticks([]), plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i][0]])
plt.show()

# Tworzenie modelu sieci neuronowej 
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10)
])

# Podsumowanie modelu
model.summary()

#Funkcja strat i metryka dokładności
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Trenowanie modelu na danych treningowych i walidacja na danych testowych
history = model.fit(train_images, train_labels, epochs=10, validation_data=(test_images, test_labels))

def predict_image(img_path):
    
    """
    Funkcja przewidująca klasę dla podanego obrazu i wyświetlająca go z nazwą przewidywanej klasy.
    """
    
    # Wczytanie i przetworzenie obrazka
    img = preprocessing.image.load_img(img_path, target_size=(32, 32))
    img_array = preprocessing.image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Przewidywanie co znajduje sie na obrazku
    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]

    # Wyświetlanie
    plt.imshow(img)
    plt.title(f'Predicted: {predicted_class}')
    plt.axis('off')
    plt.show()

img_path = 'C:/Users/daria/Documents/studia/NAI/NAI/zaba.jpg'
predict_image(img_path)



