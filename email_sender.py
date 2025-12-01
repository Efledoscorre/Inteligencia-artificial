import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta

class EnviadorEmail:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        
    def enviar_relatorio(self, arquivo_pdf, email_destinatario, metricas, duracao_sessao, 
                        email_remetente=None, senha_remetente=None):
        """Envia relatório PDF por email"""
        
        # Configurações do email (pode ser configurado via variáveis de ambiente)
        if not email_remetente:
            email_remetente = os.getenv('EMAIL_REMETENTE', 'caiobiscas@gmail.com')
        if not senha_remetente:
            senha_remetente = os.getenv('SENHA_EMAIL', '[PEGAR A CHAVE COM O CAIO]') # GERAR SENHA PORA AQUI: https://myaccount.google.com/apppasswords
            
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = email_remetente
        msg['To'] = email_destinatario
        msg['Subject'] = f"Relatório de Análise Comportamental - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        # Corpo do email
        corpo_email = self._criar_corpo_email(metricas, duracao_sessao)
        msg.attach(MIMEText(corpo_email, 'html'))
        
        # Anexar PDF
        with open(arquivo_pdf, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.basename(arquivo_pdf)}'
        )
        msg.attach(part)
        
        # Enviar email
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(email_remetente, senha_remetente)
            text = msg.as_string()
            server.sendmail(email_remetente, email_destinatario, text)
            server.quit()
            return True
        except Exception as e:
            raise Exception(f"Erro ao enviar email: {str(e)}")
    
    def _criar_corpo_email(self, metricas, duracao_sessao):
        """Cria corpo HTML do email"""
        total_tempo = sum(metricas.values())
        
        # Resumo das métricas
        resumo_metricas = ""
        for postura, tempo in metricas.items():
            percentual = (tempo / total_tempo) * 100 if total_tempo > 0 else 0
            tempo_formatado = str(timedelta(seconds=int(tempo)))
            resumo_metricas += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">{postura.replace('_', ' ').title()}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{tempo_formatado}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{percentual:.1f}%</td>
            </tr>
            """
        
        corpo = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <h2 style="color: #333;">📊 Relatório de Análise Comportamental</h2>
            
            <p>Olá,</p>
            
            <p>Segue em anexo o relatório completo da sua sessão de análise comportamental.</p>
            
            <h3 style="color: #555;">📈 Resumo da Sessão:</h3>
            <ul>
                <li><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y')}</li>
                <li><strong>Duração:</strong> {str(timedelta(seconds=int(duracao_sessao)))}</li>
                <li><strong>Horário:</strong> {datetime.now().strftime('%H:%M:%S')}</li>
            </ul>
            
            <h3 style="color: #555;">📋 Métricas Principais:</h3>
            <table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Postura</th>
                    <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Tempo</th>
                    <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Percentual</th>
                </tr>
                {resumo_metricas}
            </table>
            
            <p style="margin-top: 20px;">
                📎 <strong>Anexo:</strong> Relatório completo em PDF com gráficos detalhados.
            </p>
            
            <hr style="margin: 20px 0;">
            <p style="color: #666; font-size: 12px;">
                Este email foi gerado automaticamente pelo sistema de análise comportamental.<br>
                Para dúvidas, entre em contato conosco.
            </p>
        </body>
        </html>
        """
        
        return corpo