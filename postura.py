import mediapipe as mp
import numpy as np
import pickle

mp_pose = mp.solutions.pose

# =============== CARREGAR MODELO BRACOS CRUZADOS ==================

try:
    modelo_bracos = pickle.load(open("modelo_bracos.pkl", "rb"))
    encoder_bracos = pickle.load(open("label_encoder.pkl", "rb"))
    IA_BRACOS_ATIVA = True
except:
    print("[AVISO] Modelo IA de bracos cruzados nao encontrado!")
    IA_BRACOS_ATIVA = False


# =============== CARREGAR MODELO MAOS ESCONDIDAS ==================

try:
    modelo_maos = pickle.load(open("modelo_maos_escondidas.pkl", "rb"))
    encoder_maos = pickle.load(open("label_maos_escondidas_encoder.pkl", "rb"))
    IA_MAOS_ATIVA = True
except:
    print("[AVISO] Modelo IA de maos escondidas nao encontrado!")
    IA_MAOS_ATIVA = False


# =============== CARREGAR MODELO CABECA BAIXA ==================

try:
    modelo_cabeca = pickle.load(open("modelo_cabeca_baixa.pkl", "rb"))
    encoder_cabeca = pickle.load(open("label_cabeca_baixa_encoder.pkl", "rb"))
    IA_CABECA_ATIVA = True
except:
    print("[AVISO] Modelo IA de cabeca baixa nao encontrado!")
    IA_CABECA_ATIVA = False


# ==================================================================
# Função auxiliar para transformar landmarks em vetor 1D
# ==================================================================

def landmarks_para_vetor(landmarks):
    vetor = []
    for lm in landmarks:
        vetor.extend([lm.x, lm.y, lm.z])
    return np.array(vetor).reshape(1, -1)


# ==================================================================
# Função — Braços Cruzados
# ==================================================================

def bracos_cruzados(landmarks):

    if not IA_BRACOS_ATIVA:
        return False

    vetor = landmarks_para_vetor(landmarks)

    pred = modelo_bracos.predict(vetor)[0]
    label = encoder_bracos.inverse_transform([pred])[0]

    return label == "bracos_cruzados"


# ==================================================================
# Função — Mãos Escondidas
# ==================================================================

def maos_escondidas(landmarks):

    if not IA_MAOS_ATIVA:
        return False

    vetor = landmarks_para_vetor(landmarks)

    pred = modelo_maos.predict(vetor)[0]
    label = encoder_maos.inverse_transform([pred])[0]

    return label == "maos_escondidas"


# ==================================================================
# Função — Cabeça Baixa
# ==================================================================

def cabeca_baixa(landmarks):

    if not IA_CABECA_ATIVA:
        return False

    vetor = landmarks_para_vetor(landmarks)

    pred = modelo_cabeca.predict(vetor)[0]
    label = encoder_cabeca.inverse_transform([pred])[0]

    return label == "cabeca_baixa"
