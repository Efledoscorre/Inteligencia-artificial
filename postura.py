import mediapipe as mp
import numpy as np
import pickle

# Carrega modelo IA
try:
    modelo_ml = pickle.load(open("modelo_bracos.pkl", "rb"))
    IA_ATIVA = True
except:
    print("[AVISO] Modelo IA nao encontrado!")
    IA_ATIVA = False

mp_pose = mp.solutions.pose


def bracos_cruzados(landmarks):
    """
    IA pura — usa somente o modelo ML treinado.
    Retorna True se a IA identificar braços cruzados.
    """

    if not IA_ATIVA:
        return False  # impede erro caso o modelo não exista

    vetor = []

    # Monta vetor com os 99 valores (x,y,z dos 33 landmarks)
    for lm in landmarks:
        vetor.extend([lm.x, lm.y, lm.z])

    vetor = np.array(vetor).reshape(1, -1)

    # Predição
    pred = modelo_ml.predict(vetor)[0]

    # dependendo do treinamento, o label pode ser string ou número

    return pred == 0
