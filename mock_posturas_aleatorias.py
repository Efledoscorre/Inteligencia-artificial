import random
import cv2

class MockMetricasPosturas:
    def __init__(self):
        self.probabilidades = {
            "bracos_cruzados": 0.15,    # 15%
            "maos_escondidas": 0.25,    # 10% (0.15 + 0.10)
            "cabeca_baixa": 0.35        # 10% (0.25 + 0.10)
        }
        
    def detectar_postura_mock(self, frame):
        """Simula detecção de posturas com probabilidades realistas"""
        rand = random.random()
        
        if rand < self.probabilidades["bracos_cruzados"]:
            cv2.putText(frame, "Bracos cruzados detectados (MOCK)",
                       (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return "bracos_cruzados"
            
        elif rand < self.probabilidades["maos_escondidas"]:
            cv2.putText(frame, "Maos escondidas detectadas (MOCK)",
                       (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            return "maos_escondidas"
            
        elif rand < self.probabilidades["cabeca_baixa"]:
            cv2.putText(frame, "Cabeca baixa detectada (MOCK)",
                       (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            return "cabeca_baixa"
            
        return "postura_normal"