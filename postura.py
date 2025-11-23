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

def dist(a, b):
    """Calcula a distância euclidiana entre dois landmarks."""
    return ((a.x - b.x)**2 + (a.y - b.y)**2)**0.5

def bracos_cruzados(landmarks):
    """
    Retorna True se os braços estiverem cruzados.
    O parâmetro limite_dist ajusta a sensibilidade da detecção.
    """
 # Pega os landmarks importantes
    mao_esq = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    mao_dir = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    cotovelo_esq = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    cotovelo_dir = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    ombro_esq = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    ombro_dir = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

    # ---------------------------
    #   REGRA 1 — Versão robusta (cruzamento natural na frente do tronco)
    # ---------------------------
    cruz_esq = dist(mao_esq, cotovelo_dir) < dist(mao_esq, cotovelo_esq)
    cruz_dir = dist(mao_dir, cotovelo_esq) < dist(mao_dir, cotovelo_dir)
    maos_proximas = dist(mao_esq, mao_dir) < 0.15
    cotovelos_baixos = (cotovelo_esq.y > ombro_esq.y and
                        cotovelo_dir.y > ombro_dir.y)

    cruzamento_natural = cruz_esq and cruz_dir and maos_proximas and cotovelos_baixos

    # ---------------------------
    #   REGRA 2 — Mão tocando ombro oposto
    # ---------------------------
    toque_ombro = (
        dist(mao_esq, ombro_dir) < 0.2 or   # mão esquerda → ombro direito
        dist(mao_dir, ombro_esq) < 0.2      # mão direita → ombro esquerdo
    )

    # Resultado final: se qualquer padrão ocorrer → braços cruzados
    return cruzamento_natural or toque_ombro
