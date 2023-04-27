import cv2
import mediapipe as mp
import random
#MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
# Lógica para determinar o formato da mão (pedra, papel ou tesoura) com base nas coordenadas dos dedos
def determine_hand_gesture(finger_coordinates):
    
    # Retorna um formato aleatório apenas para exemplo
    return random.choice(["Pedra", "Papel", "Tesoura"])  
def determine_winner(hand1_gesture, hand2_gesture):
    if hand1_gesture == hand2_gesture:
        return "Empate", None
    if hand1_gesture == "Pedra":
        if hand2_gesture == "Tesoura":
            return "Mao 1", "Pedra"
        elif hand2_gesture == "Papel":
            return "Mao 2", "Papel"
    if hand1_gesture == "Papel":
        if hand2_gesture == "Pedra":
            return "Mao 1", "Papel"
        elif hand2_gesture == "Tesoura":
            return "Mao 2", "Tesoura"
    if hand1_gesture == "Tesoura":
        if hand2_gesture == "Papel":
            return "Mao 1", "Tesoura"
        elif hand2_gesture == "Pedra":
            return "Mao 2", "Pedra"
    return None, None
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=0, max_num_hands=2, min_detection_confidence=0.5)
# Captura de vídeo da webcam (altere o valor para o caminho do vídeo, se necessário)
cap = cv2.VideoCapture('pedra-papel-tesoura.mp4')  
# Inicialização dos placares
score_player1 = 0
score_player2 = 0
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    player1_gesture = None
    player2_gesture = None
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            finger_coordinates = []
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                finger_coordinates.append((x, y))
            hand_gesture = determine_hand_gesture(finger_coordinates)
            if i == 0:
                player1_gesture = hand_gesture
            elif i == 1:
                player2_gesture = hand_gesture
            if hand_gesture:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2
                ),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2),
            )
            cv2.putText(
                image,
                hand_gesture,
                (int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * image.shape[1]),
                 int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * image.shape[0])),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
    winner, winning_gesture = determine_winner(player1_gesture, player2_gesture)
    if winner:
        cv2.putText(
            image,
            "Vencedor: {} - {}".format(winner, winning_gesture),
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )
        if winner == "Mao 1":
            score_player1 += 1
        else:
            score_player2 += 1
    # Exibir o placar dos jogadores
    cv2.putText(
        image,
        "Placar - Mao 1: {}  Mao 2: {}".format(score_player1, score_player2),
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.imshow("Pedra-Papel-Tesoura", image)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
