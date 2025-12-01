import cv2

class DashboardComportamental:
    def __init__(self):
        self.cores = {
            "postura_normal": (0, 255, 0),     # Verde
            "bracos_cruzados": (0, 0, 255),    # Vermelho
            "maos_escondidas": (255, 0, 0),    # Azul
            "cabeca_baixa": (0, 255, 255)      # Amarelo
        }
        
    def desenhar_dashboard(self, frame, metricas, tempo_total, postura_atual):
        """Desenha o dashboard de métricas em tempo real no frame"""
        h, w = frame.shape[:2]
        
        # Área do dashboard (canto superior direito)
        dash_w, dash_h = 350, 200
        dash_x, dash_y = w - dash_w - 10, 10
        
        # Fundo semi-transparente
        overlay = frame.copy()
        cv2.rectangle(overlay, (dash_x, dash_y), (dash_x + dash_w, dash_y + dash_h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Título do dashboard
        cv2.putText(frame, "DASHBOARD COMPORTAMENTAL", (dash_x + 10, dash_y + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Tempo: {int(tempo_total)}s", (dash_x + 10, dash_y + 45), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Barras de progresso
        self._desenhar_barras_progresso(frame, dash_x, dash_y, metricas, tempo_total)
        
        # Indicador de postura atual
        cv2.putText(frame, f"Atual: {postura_atual.replace('_', ' ').title()}", 
                   (dash_x + 10, dash_y + dash_h - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.cores.get(postura_atual, (255, 255, 255)), 1)
    
    def _desenhar_barras_progresso(self, frame, dash_x, dash_y, metricas, tempo_total):
        """Desenha as barras de progresso para cada postura"""
        y_offset = 65
        bar_width = 200
        bar_height = 15
        
        for i, (postura, tempo) in enumerate(metricas.items()):
            y_pos = dash_y + y_offset + (i * 30)
            
            # Percentual
            percentual = (tempo / tempo_total) * 100 if tempo_total > 0 else 0
            
            # Nome da postura
            nome = postura.replace('_', ' ').title()[:12]  # Limita tamanho
            cv2.putText(frame, f"{nome}", (dash_x + 10, y_pos + 12), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
            
            # Barra de fundo
            cv2.rectangle(frame, (dash_x + 120, y_pos), 
                         (dash_x + 120 + bar_width, y_pos + bar_height), (50, 50, 50), -1)
            
            # Barra de progresso
            progress_width = int((percentual / 100) * bar_width)
            if progress_width > 0:
                cv2.rectangle(frame, (dash_x + 120, y_pos), 
                             (dash_x + 120 + progress_width, y_pos + bar_height), 
                             self.cores[postura], -1)
            
            # Percentual texto
            cv2.putText(frame, f"{percentual:.1f}%", (dash_x + 330, y_pos + 12), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)