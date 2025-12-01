import openai
import os
from datetime import timedelta

class FeedbackIA:
    def __init__(self):
        # Configuração da API (será definida via variável de ambiente)
        openai.api_key = os.getenv('OPENAI_API_KEY', '[PEGAR A CHAVE COM O CAIO DEPOIS]')
        
        # Role prompting - Define o papel da IA
        self.system_prompt = """
        Você é um PSICÓLOGO COMPORTAMENTAL ESPECIALISTA em análise de linguagem corporal e comunicação não-verbal.

        ESPECIALIZAÇÃO:
        - Análise de posturas corporais e seus significados psicológicos
        - Identificação de padrões comportamentais em ambientes profissionais
        - Coaching para melhoria da comunicação não-verbal
        - Desenvolvimento de soft skills e presença executiva

        O QUE VOCÊ RECEBERÁ:
        - Métricas temporais de posturas corporais detectadas durante uma sessão
        - Percentuais de tempo gasto em cada postura específica
        - Duração total da análise comportamental

        O QUE VOCÊ DEVE RESPONDER:
        1. ANÁLISE COMPORTAMENTAL: Interpretação psicológica das posturas detectadas
        2. PONTOS DE ATENÇÃO: Identificação de padrões problemáticos
        3. RECOMENDAÇÕES PRÁTICAS: Dicas específicas e acionáveis para melhoria
        4. PLANO DE DESENVOLVIMENTO: Sugestões de exercícios e práticas

        DIRETRIZES:
        - Seja empático e construtivo, nunca crítico
        - Forneça insights baseados em psicologia comportamental
        - Dê exemplos práticos e exercícios específicos
        - Mantenha tom profissional mas acessível
        - Foque em desenvolvimento e crescimento pessoal
        """
    
    def gerar_feedback(self, metricas, duracao_sessao):
        """Gera feedback personalizado baseado nas métricas comportamentais"""
        
        # Preparar dados para a IA
        dados_sessao = self._formatar_metricas(metricas, duracao_sessao)
        
        # Prompt específico com os dados
        user_prompt = f"""
        Analise os seguintes dados comportamentais de uma sessão de {str(timedelta(seconds=int(duracao_sessao)))}:

        MÉTRICAS DETECTADAS:
        {dados_sessao}

        Por favor, forneça uma análise completa seguindo sua especialização em psicologia comportamental.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return self._feedback_fallback(metricas, duracao_sessao, str(e))
    
    def _formatar_metricas(self, metricas, duracao_sessao):
        """Formata métricas para envio à IA"""
        total_tempo = sum(metricas.values())
        
        dados = []
        for postura, tempo in metricas.items():
            percentual = (tempo / total_tempo) * 100 if total_tempo > 0 else 0
            tempo_formatado = str(timedelta(seconds=int(tempo)))
            
            # Traduzir posturas para linguagem mais clara
            postura_legivel = {
                "postura_normal": "Postura Normal/Neutra",
                "bracos_cruzados": "Braços Cruzados (postura defensiva)",
                "maos_escondidas": "Mãos Escondidas (possível insegurança)",
                "cabeca_baixa": "Cabeça Baixa (desatenção/introversão)"
            }.get(postura, postura)
            
            dados.append(f"• {postura_legivel}: {tempo_formatado} ({percentual:.1f}%)")
        
        return "\n".join(dados)
    
    def _feedback_fallback(self, metricas, duracao_sessao, erro):
        """Feedback básico caso a API falhe"""
        total_tempo = sum(metricas.values())
        
        feedback = f"""
        ⚠️ Feedback Básico (API indisponível: {erro})
        
        📊 ANÁLISE RÁPIDA DA SESSÃO:
        Duração: {str(timedelta(seconds=int(duracao_sessao)))}
        
        """
        
        # Análise simples baseada em regras
        for postura, tempo in metricas.items():
            percentual = (tempo / total_tempo) * 100 if total_tempo > 0 else 0
            
            if postura == "bracos_cruzados" and percentual > 20:
                feedback += "🔴 ATENÇÃO: Alto tempo com braços cruzados pode indicar postura defensiva.\n"
            elif postura == "cabeca_baixa" and percentual > 15:
                feedback += "🟡 OBSERVAÇÃO: Cabeça baixa frequente pode sugerir falta de confiança.\n"
            elif postura == "maos_escondidas" and percentual > 10:
                feedback += "🟠 NOTA: Mãos escondidas podem indicar nervosismo.\n"
        
        feedback += "\n💡 RECOMENDAÇÃO: Configure a API do OpenAI para feedback personalizado completo."
        
        return feedback