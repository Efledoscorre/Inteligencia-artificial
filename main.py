import cv2
import mediapipe as mp
import postura
import time
import random
from datetime import datetime, timedelta
from dashboard import DashboardComportamental
from relatorio_pdf import GeradorRelatorioPDF
from email_sender import EnviadorEmail
from feedback_ia import FeedbackIA
from mock_posturas_aleatorias import MockMetricasPosturas

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Sistema de métricas temporais
metricas = {
    "bracos_cruzados": 0.0,
    "maos_escondidas": 0.0, 
    "cabeca_baixa": 0.0,
    "postura_normal": 0.0
}

inicio_sessao = time.time()
ultimo_frame_time = time.time()
postura_atual = "postura_normal"

# Inicializar dashboard, gerador de PDF, enviador de email e IA
dashboard = DashboardComportamental()
gerador_pdf = GeradorRelatorioPDF()
enviador_email = EnviadorEmail()
feedback_ia = FeedbackIA()
mock_posturas = MockMetricasPosturas()

# Configuração de email (pode ser alterada aqui ou via variáveis de ambiente)
EMAIL_DESTINATARIO = "seuEMailAqui@gmail.com"  # AQUI E O EMAIL DE QUEM VAI RECEBER O PDF


with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(img_rgb)

        # Atualizar métricas temporais
        tempo_atual = time.time()
        delta_tempo = tempo_atual - ultimo_frame_time
        metricas[postura_atual] += delta_tempo
        ultimo_frame_time = tempo_atual

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                result.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            landmarks = result.pose_landmarks.landmark
            nova_postura = "postura_normal"

            # ==========================
            # MODO MOCK - PARA TESTES
            # ==========================
            # nova_postura = mock_posturas.detectar_postura_mock(frame)

            # ==========================
            # IA — Braços Cruzados
            # ==========================
            if postura.bracos_cruzados(landmarks):
                cv2.putText(frame, "Bracos cruzados detectados (IA)",
                            (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2)
                # nova_postura = "bracos_cruzados"

            # ==========================
            # IA — Mãos Escondidas
            # ==========================
            elif postura.maos_escondidas(landmarks):
                cv2.putText(frame, "Maos escondidas detectadas (IA)",
                            (10, 80), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 0), 2)
                # nova_postura = "maos_escondidas"

            # ==========================
            # IA — Cabeça Baixa
            # ==========================
            if postura.cabeca_baixa(landmarks):
                cv2.putText(frame, "Cabeca baixa detectada (IA)",
                            (10, 120), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 255), 2)
                # if nova_postura == "postura_normal":
                #     nova_postura = "cabeca_baixa"

            # postura_atual = nova_postura Descomentar aqui se for usar o mock de posturas

        # Dashboard em tempo real
        tempo_total = tempo_atual - inicio_sessao
        dashboard.desenhar_dashboard(frame, metricas, tempo_total, postura_atual)

        cv2.imshow("Pose Estimation", frame)

        # Verifica se tecla 'q' foi pressionada
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
            
        # Verifica se janela foi fechada
        try:
            if cv2.getWindowProperty("Pose Estimation", cv2.WND_PROP_VISIBLE) < 1:
                break
        except cv2.error:
            break


cap.release()
cv2.destroyAllWindows()

# Gerar relatório PDF automaticamente
fim_sessao = time.time()
tempo_total_sessao = fim_sessao - inicio_sessao

print("\n" + "="*50)
print("         GERANDO RELATÓRIO PDF...")
print("="*50)

try:
    # Gerar feedback da IA primeiro
    print("🤖 Gerando feedback personalizado da IA...")
    feedback = feedback_ia.gerar_feedback(metricas, tempo_total_sessao)
    
    # Gerar PDF com feedback da IA incluído
    nome_arquivo = gerador_pdf.gerar_relatorio(metricas, inicio_sessao, fim_sessao, feedback)
    print(f"✅ Relatório PDF gerado com feedback IA: {nome_arquivo}")
    
    # Enviar por email
    print("📧 Enviando relatório por email...")
    try:
        enviador_email.enviar_relatorio(
            arquivo_pdf=nome_arquivo,
            email_destinatario=EMAIL_DESTINATARIO,
            metricas=metricas,
            duracao_sessao=tempo_total_sessao
        )
        print(f"✅ Email enviado com sucesso para: {EMAIL_DESTINATARIO}")
    except Exception as email_error:
        print(f"⚠️ Erro ao enviar email: {email_error}")
        print("💡 Configure as variáveis: EMAIL_REMETENTE e SENHA_EMAIL")
        print("📁 Relatório salvo localmente")
    
    print(f"📊 Duração da sessão: {str(timedelta(seconds=int(tempo_total_sessao)))}")

    
except Exception as e:
    print(f"❌ Erro ao gerar relatório: {e}")
    print("💡 Instale: pip install reportlab")