# coletar_bracos_cruzados.py
import cv2
import mediapipe as mp
import csv
import os
from datetime import datetime

# Configurações
CSV_OUT = "dataset_bracos_cruzados.csv"
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
        # 33 landmarks * 3 (x,y,z)
        for i in range(33):
            header += [f"x{i}", f"y{i}", f"z{i}"]
        header.append("label")
        with open(path, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)

criar_csv_se_nao_existe(CSV_OUT)

# Função para escrever uma linha (landmarks normalizados + label)
def salvar_landmarks_csv(path, landmarks, label):
    row = []
    for lm in landmarks:
        row += [lm.x, lm.y, lm.z]
    row.append(label)
    with open(path, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

# Contadores para feedback
contadores = {"bracos_cruzados": 0, "nao_cruzados": 0}

# Se o CSV já contém linhas, podemos contar exemplos já existentes
if os.path.exists(CSV_OUT):
    try:
        with open(CSV_OUT, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # pula header
            for r in reader:
                if len(r) > 0:
                    label = r[-1]
                    if label in contadores:
                        contadores[label] += 1
    except Exception:
        pass

# Estado inicial do rótulo (por padrão coletar "bracos_cruzados" primeiro)
label_atual = "bracos_cruzados"

cap = cv2.VideoCapture(WEBCAM_INDEX)
if not cap.isOpened():
    raise RuntimeError(f"Não foi possível abrir a webcam (índice {WEBCAM_INDEX})")

with mp_pose.Pose(min_detection_confidence=MIN_DETECTION_CONF,
                  min_tracking_confidence=MIN_TRACKING_CONF) as pose:

    print("Iniciando coleta. Teclas: [c] bracos_cruzados, [n] nao_cruzados, [q] sair")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao ler frame. Encerrando.")
            break

        # Espelho opcional (se preferir ver como espelho, descomente)
        # frame = cv2.flip(frame, 1)

        # Converte e processa
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(img_rgb)

        # Se detectou landmarks, desenha e possibilita salvar
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Mostra contadores e rótulo atual na tela
            info_text = f"Label atual: {label_atual}  |  saved: cruzados={contadores['bracos_cruzados']} nao={contadores['nao_cruzados']}"
            cv2.putText(frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        else:
            cv2.putText(frame, "Nenhuma pose detectada", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("Coleta - pressione c/n para rotular, q para sair", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):          # definir rótulo atual como cruzado (e salvar este frame)
            label_atual = "bracos_cruzados"
            if result.pose_landmarks:
                salvar_landmarks_csv(CSV_OUT, result.pose_landmarks.landmark, label_atual)
                contadores[label_atual] += 1
                print(f"Salvo exemplo {contadores[label_atual]} para {label_atual}")
        elif key == ord('n'):        # definir rótulo atual como nao cruzado (e salvar)
            label_atual = "nao_cruzados"
            if result.pose_landmarks:
                salvar_landmarks_csv(CSV_OUT, result.pose_landmarks.landmark, label_atual)
                contadores[label_atual] += 1
                print(f"Salvo exemplo {contadores[label_atual]} para {label_atual}")

cap.release()
cv2.destroyAllWindows()
print("Coleta finalizada.")
