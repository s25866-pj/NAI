import cv2
import mediapipe as mp

# Inicjalizacja modułu MediaPipe dla rąk
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Otwórz kamerę
kamera = cv2.VideoCapture(0)

if not kamera.isOpened():
    print("Nie udało się otworzyć kamery.")
else:
    while True:
        ret, frame = kamera.read()
        if not ret:
            print("Nie udało się odczytać obrazu z kamery.")
            break

        # Konwersja obrazu do RGB (MediaPipe używa RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Przetwarzanie klatki
        result = hands.process(rgb_frame)

        # Rysowanie wykrytych punktów i krawędzi dłoni
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Wyświetlanie obrazu z nałożonymi wynikami
        cv2.imshow("Wykrywanie dłoni", frame)

        # Naciśnięcie 'q' kończy pętlę
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Zwolnienie zasobów
kamera.release()
cv2.destroyAllWindows()
