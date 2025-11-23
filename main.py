import cv2
import mediapipe as mp
import postura

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(img_rgb)

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                result.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            landmarks = result.pose_landmarks.landmark

            # IA 100%
            if postura.bracos_cruzados(landmarks):
                cv2.putText(frame, "Bracos cruzados detectados (IA)", 
                            (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (0, 0, 255), 2)

        cv2.imshow("Pose Estimation", frame)

        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
