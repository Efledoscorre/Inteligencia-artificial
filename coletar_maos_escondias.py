# coletar_maos.py
import cv2
import mediapipe as mp
import csv
import os
from datetime import datetime

# Configurações
CSV_OUT = "dataset_maos_escondidas.csv"
WEBCAM_INDEX = 0
MIN_DETECTION_CONF = 0.5
MIN_TRACKING_CONF = 0.5

# Inicializa mediapipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Cria arquivo CSV se não existir e escreve cabeçalho
def criar_csv_se_nao_existe(path):
    if not os.path.exists(path):
        header = []
        for i in range(33):
            header += [f"x{i}", f"y{i}", f"z{i}"]
        header.append("label")
        with open(path, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)

criar_csv_se_nao_existe(CSV_OUT)

# Função para salvar landmarks
def salvar_landmarks_csv(path, landmarks, label):
    row = []
    for lm in landmarks:
        row += [lm.x, lm.y, lm.z]
    row.append(label)
    with open(path, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

# Contadores
contadores = {"maos_escondidas": 0, "maos_visiveis": 0}

# Se já existe CSV, conta quantos exemplos de cada classe já existem
if os.path.exists(CSV_OUT):
    try:
        with open(CSV_OUT, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader)
            for r in reader:
                if len(r) > 0:
                    label = r[-1]
                    if label in contadores:
                        contadores[label] += 1
    except:
        pass

# Rótulo inicial
label_atual = "maos_escondidas"

cap = cv2.VideoCapture(WEBCAM_INDEX)
if not cap.isOpened():
    raise RuntimeError("Não foi possível abrir a webcam")

with mp_pose.Pose(min_detection_confidence=MIN_DETECTION_CONF,
                  min_tracking_confidence=MIN_TRACKING_CONF) as pose:

    print("Iniciando coleta. Teclas: [c] maos_escondidas, [n] maos_visiveis, [q] sair")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(img_rgb)

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            info_text = (f"Label atual: {label_atual}  |  "
                         f"maos_escondidas={contadores['maos_escondidas']}  "
                         f"maos_visiveis={contadores['maos_visiveis']}")

            cv2.putText(frame, info_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Coleta", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        elif key == ord('c'):
            label_atual = "maos_escondidas"
            if result.pose_landmarks:
                salvar_landmarks_csv(CSV_OUT, result.pose_landmarks.landmark, label_atual)
                contadores[label_atual] += 1
                print(f"Salvo {contadores[label_atual]} exemplos de {label_atual}")

        elif key == ord('n'):
            label_atual = "maos_visiveis"
            if result.pose_landmarks:
                salvar_landmarks_csv(CSV_OUT, result.pose_landmarks.landmark, label_atual)
                contadores[label_atual] += 1
                print(f"Salvo {contadores[label_atual]} exemplos de {label_atual}")

cap.release()
cv2.destroyAllWindows()
print("Coleta finalizada!")
