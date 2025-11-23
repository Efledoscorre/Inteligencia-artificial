import mediapipe as mp

mp_pose = mp.solutions.pose

def detectar_ombros_caidos(landmarks):
    """
    Detecta se os ombros estão caídos comparando a posição vertical
    da orelha com o ombro correspondente.
    """

    orelha_esq = landmarks[mp_pose.PoseLandmark.LEFT_EAR]
    orelha_dir = landmarks[mp_pose.PoseLandmark.RIGHT_EAR]
    ombro_esq = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    ombro_dir = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    #Calcula o quanto o ombro está abaixo da orelha. x(horinzontal), y(vertical), z(profunidade da imagem)
    dif_esq = ombro_esq.y - orelha_esq.y
    dif_dir = ombro_dir.y - orelha_dir.y

    LIMITE = 0.30  # pode ajustar depois

    #Retorna 2 valores ao mesmo tempo separados por vírgula (retorna uma tupla) Ex.: (True, False)
    return dif_esq > LIMITE, dif_dir > LIMITE


def bracos_cruzados(landmarks, limite_dist=0.12):
    """
    Retorna True se os braços estiverem cruzados.
    O parâmetro limite_dist ajusta a sensibilidade da detecção.
    """

    # atalhos para facilitar
    ombro_dir = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    ombro_esq = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    punho_dir = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    punho_esq = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    cotovelo_dir = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    cotovelo_esq = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]

    # Distância entre dois pontos (em coordenadas normalizadas)
    def dist(a, b):
        return ((a.x - b.x)**2 + (a.y - b.y)**2)**0.5

    # 1. Punho direito próximo do ombro esquerdo
    direita_cruza = dist(punho_dir, ombro_esq) < limite_dist

    # 2. Punho esquerdo próximo do ombro direito
    esquerda_cruza = dist(punho_esq, ombro_dir) < limite_dist

    # 3. Cotovelos próximos (reforça a detecção)
    cotovelos_proximos = dist(cotovelo_dir, cotovelo_esq) < limite_dist * 1.2

    # Resultado final
    return (direita_cruza and esquerda_cruza) or cotovelos_proximos

