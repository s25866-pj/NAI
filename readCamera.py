import cv2
import mediapipe as mp
import webbrowser

# Inicjalizacja modułu MediaPipe dla rąk
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

def gesture_recognition(hand_landmarks):
    # Górne punkty palców u dłoni
    PUNKT_KCIUK = 4
    PUNKT_WSKAZUJACY = 8
    PUNKT_SRODKOWY = 12
    PUNKT_SERDECZNY = 16
    PUNKT_MALY = 20

    # Podstawy palców
    PODSTAWA_KCIUKA = 2
    PODSTAWA_WSKAZUJACEGO = 5
    PODSTAWA_SRODKOWEGO = 9
    PODSTAWA_SERDECZNEGO = 13
    PODSTAWA_MALEGO = 17

    # Pobranie współrzędnych punktów
    landmarks = hand_landmarks.landmark

    # Kciuk
    if landmarks[PUNKT_KCIUK].y < landmarks[PODSTAWA_KCIUKA].y:  # Kciuk wyprostowany 
        kciuk = True
    else:
        kciuk = False

    # Palec wskazujący
    if landmarks[PUNKT_WSKAZUJACY].y < landmarks[PODSTAWA_WSKAZUJACEGO].y: 
        wskazujacy = True
    else:
        wskazujacy = False

    # Palec środkowy
    if landmarks[PUNKT_SRODKOWY].y < landmarks[PODSTAWA_SRODKOWEGO].y:
        srodkowy = True
    else:
        srodkowy = False

    # Palec serdeczny
    if landmarks[PUNKT_SERDECZNY].y < landmarks[PODSTAWA_SERDECZNEGO].y:
        serdeczny = True
    else:
        serdeczny = False

    # Mały palec
    if landmarks[PUNKT_MALY].y < landmarks[PODSTAWA_MALEGO].y:
        maly = True
    else:
        maly = False

    # Rozpoznawanie gestów na podstawie kombinacji palców
    if kciuk and not wskazujacy and not srodkowy and not serdeczny and not maly:
        return "Thumbs up"  
    elif wskazujacy and not srodkowy and not serdeczny and not maly and not kciuk:
        return "Index finger up"
    elif maly and not wskazujacy and not srodkowy and not serdeczny and not kciuk:
        return "Little finger up"
    elif wskazujacy and srodkowy and serdeczny and maly and kciuk:
        return "Open hand"


# Otwórz kamerę
kamera = cv2.VideoCapture(0)
przegladarka_otwarta = False
if not kamera.isOpened():
    print("Nie udało się otworzyć kamery.")
else:
    przegladarka_otwarta = False
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

                # Rozpoznawanie gestu
                gest = gesture_recognition(hand_landmarks)

                if gest == "Thumbs up" and przegladarka_otwarta is False:
                    print("Otwieram przeglądarkę")
                    webbrowser.open("https://www.google.com") 
                    przegladarka_otwarta = True

                if gest == "Index finger up":
                    print("Zamykam program...")
                    exit() # Wyjście z programu

                if gest == "Little finger up":
                    print("Pauza. Naciśnij 's', aby zakończyć.")
                    cv2.waitKey(0)  # Wstrzymanie działania do czasu naciśnięcia dowolnego klawisza

                if gest == "Open hand":
                    cv2.putText(frame, "OPEN HAND", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (219, 48, 130), 5) # Wyświetlanie gestu na kamerze


        # Wyświetlanie obrazu z nałożonymi wynikami
        cv2.imshow("Wykrywanie dłoni", frame)

        # Naciśnięcie 'q' kończy pętlę
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Zwolnienie zasobów
kamera.release()
cv2.destroyAllWindows()
