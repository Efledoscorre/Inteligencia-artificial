import cv2
import mediapipe as mp
import postura

mp_drawing = mp.solutions.drawing_utils        # Função de desenho
mp_pose = mp.solutions.pose                   # Modelo de pose

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Converte para RGB (MediaPipe usa RGB)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Processa os pontos do corpo -> Result é um objeto que possui tudo o que o mp conseguiu detectar no frame
        result = pose.process(img_rgb)

        # Se encontrou a pose
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,                              # imagem onde desenha
                result.pose_landmarks,              # pontos detectados
                mp_pose.POSE_CONNECTIONS            # conexões entre pontos
            )

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

        if postura.bracos_cruzados(landmarks):
            cv2.putText(frame, "Evite cruzar os bracos ao apresentar!", 
                    (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 0, 255), 2)


        cv2.imshow("Pose Estimation", frame)

        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
