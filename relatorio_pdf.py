from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from datetime import datetime, timedelta
import os

class GeradorRelatorioPDF:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._criar_estilos_customizados()
        
    def _criar_estilos_customizados(self):
        """Cria estilos customizados seguindo melhores práticas de UI/UX"""
        # Paleta de cores profissional
        self.cor_primaria = colors.Color(0.2, 0.3, 0.5)  # Azul corporativo
        self.cor_secundaria = colors.Color(0.9, 0.9, 0.95)  # Azul claro
        self.cor_acento = colors.Color(0.1, 0.7, 0.3)  # Verde
        self.cor_texto = colors.Color(0.2, 0.2, 0.2)  # Cinza escuro
        
        # Título principal
        self.titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            fontName='Helvetica-Bold',
            textColor=self.cor_primaria,
            spaceAfter=40,
            spaceBefore=20,
            alignment=1,
            leading=28
        )
        
        # Subtítulos
        self.subtitulo_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            fontName='Helvetica-Bold',
            textColor=self.cor_primaria,
            spaceAfter=20,
            spaceBefore=30,
            borderWidth=0,
            borderColor=self.cor_primaria,
            borderPadding=10
        )
        
        # Texto corpo
        self.corpo_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            textColor=self.cor_texto,
            spaceAfter=12,
            leading=16
        )
        
    def gerar_relatorio(self, metricas, inicio_sessao, fim_sessao, feedback_ia=None, nome_arquivo=None):
        """Gera relatório PDF com métricas comportamentais"""
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"relatorio_comportamental_{timestamp}.pdf"
        
        # Criar documento
        doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
        story = []
        
        # Cabeçalho com design melhorado
        story.extend(self._criar_cabecalho())
        story.append(Spacer(1, 30))
        
        # Informações da sessão com design melhorado
        story.append(Paragraph("Informações da Sessão", self.subtitulo_style))
        info_sessao = self._criar_info_sessao(inicio_sessao, fim_sessao)
        story.append(info_sessao)
        story.append(Spacer(1, 30))
        
        # Gráfico de pizza melhorado
        story.append(Paragraph("Distribuição de Posturas", self.subtitulo_style))
        grafico = self._criar_grafico_pizza_melhorado(metricas)
        story.append(grafico)
        story.append(Spacer(1, 30))
        
        # Tabela de métricas melhorada
        story.append(Paragraph("Métricas Detalhadas", self.subtitulo_style))
        tabela = self._criar_tabela_metricas_melhorada(metricas)
        story.append(tabela)
        
        # Feedback da IA (se disponível)
        if feedback_ia:
            story.append(PageBreak())  # Nova página para feedback
            feedback_section = self._criar_secao_feedback_ia_melhorada(feedback_ia)
            story.extend(feedback_section)
        
        # Gerar PDF
        doc.build(story)
        return nome_arquivo
    
    def _criar_cabecalho(self):
        """Cria cabeçalho com design profissional"""
        elementos = []
        
        # Título principal
        titulo = Paragraph("RELATÓRIO DE ANÁLISE COMPORTAMENTAL", self.titulo_style)
        elementos.append(titulo)
        
        # Linha decorativa
        drawing = Drawing(500, 10)
        linha = Rect(0, 4, 500, 2)
        linha.fillColor = self.cor_primaria
        linha.strokeColor = None
        drawing.add(linha)
        elementos.append(drawing)
        
        # Subtítulo
        subtitulo = Paragraph(
            "Relatório gerado automaticamente pelo sistema de análise comportamental",
            ParagraphStyle('Subtitle', parent=self.corpo_style, 
                         fontSize=10, alignment=1, textColor=colors.grey)
        )
        elementos.append(subtitulo)
        
        return elementos
    
    def _criar_info_sessao(self, inicio, fim):
        """Cria seção com informações da sessão"""
        duracao = fim - inicio
        
        data = [
            ['📅 Data da Análise', datetime.now().strftime("%d/%m/%Y")],
            ['⏰ Horário de Início', datetime.fromtimestamp(inicio).strftime("%H:%M:%S")],
            ['⏹️ Horário de Fim', datetime.fromtimestamp(fim).strftime("%H:%M:%S")],
            ['⏱️ Duração Total', str(timedelta(seconds=int(duracao)))]
        ]
        
        tabela = Table(data, colWidths=[2.5*inch, 2*inch])
        tabela.setStyle(TableStyle([
            # Estilo melhorado
            ('BACKGROUND', (0, 0), (0, -1), self.cor_secundaria),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (0, -1), self.cor_primaria),
            ('TEXTCOLOR', (1, 0), (1, -1), self.cor_texto),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('ROUNDEDCORNERS', [5, 5, 5, 5])
        ]))
        
        return tabela
    
    def _criar_grafico_pizza_melhorado(self, metricas):
        """Cria gráfico de pizza com as métricas"""
        drawing = Drawing(500, 300)
        pie = Pie()
        pie.x = 50
        pie.y = 50
        pie.width = 200
        pie.height = 200
        
        # Paleta de cores profissional
        cores_profissionais = [
            colors.Color(0.1, 0.7, 0.3),   # Verde (normal)
            colors.Color(0.9, 0.3, 0.3),   # Vermelho (braços)
            colors.Color(0.3, 0.5, 0.9),   # Azul (mãos)
            colors.Color(0.9, 0.7, 0.1)    # Amarelo (cabeça)
        ]
        
        # Dados do gráfico
        labels = []
        data = []
        total_tempo = sum(metricas.values())
        
        for postura, tempo in metricas.items():
            if tempo > 0:
                labels.append(postura.replace('_', ' ').title())
                data.append(tempo)
        
        pie.data = data
        pie.slices.strokeColor = colors.white
        pie.slices.strokeWidth = 3
        
        # Aplicar cores e efeitos
        for i in range(len(data)):
            pie.slices[i].fillColor = cores_profissionais[i % len(cores_profissionais)]
            pie.slices[i].popout = 5 if i == 0 else 0  # Destaque na maior fatia
        
        # Legenda melhorada
        legend = Legend()
        legend.x = 280
        legend.y = 150
        legend.dx = 15
        legend.dy = 15
        legend.fontName = 'Helvetica'
        legend.fontSize = 10
        legend.boxAnchor = 'w'
        legend.columnMaximum = 4
        legend.strokeWidth = 1
        legend.strokeColor = colors.lightgrey
        legend.deltax = 75
        legend.deltay = 10
        legend.autoXPadding = 5
        legend.yGap = 0
        legend.dxTextSpace = 5
        legend.alignment = 'right'
        legend.dividerLines = 1
        legend.dividerOffsY = 4.5
        legend.subCols.rpad = 30
        
        # Dados da legenda com percentuais
        legend_data = []
        for i, (label, valor) in enumerate(zip(labels, data)):
            percentual = (valor / total_tempo) * 100 if total_tempo > 0 else 0
            legend_data.append((cores_profissionais[i % len(cores_profissionais)], f"{label} ({percentual:.1f}%)"))
        
        legend.colorNamePairs = legend_data
        
        drawing.add(pie)
        drawing.add(legend)
        return drawing
    
    def _criar_tabela_metricas_melhorada(self, metricas):
        """Cria tabela detalhada com métricas"""
        total_tempo = sum(metricas.values())
        
        # Cabeçalho melhorado
        data = [['Postura Detectada', 'Duração', 'Percentual', 'Status']]
        
        # Ícones para cada postura
        icones = {
            'postura_normal': '✅',
            'bracos_cruzados': '⚠️', 
            'maos_escondidas': '🔴',
            'cabeca_baixa': '🟡'
        }
        
        # Dados com melhor formatação
        for postura, tempo in metricas.items():
            percentual = (tempo / total_tempo) * 100 if total_tempo > 0 else 0
            tempo_formatado = str(timedelta(seconds=int(tempo)))
            
            # Status baseado no percentual
            if postura == 'postura_normal':
                status = 'Excelente' if percentual > 70 else 'Bom' if percentual > 50 else 'Atenção'
            else:
                status = 'Crítico' if percentual > 30 else 'Moderado' if percentual > 15 else 'Aceitável'
            
            icone = icones.get(postura, '•')
            nome_postura = f"{icone} {postura.replace('_', ' ').title()}"
            
            data.append([
                nome_postura,
                tempo_formatado,
                f"{percentual:.1f}%",
                status
            ])
        
        tabela = Table(data, colWidths=[2.5*inch, 1.2*inch, 1*inch, 1.3*inch])
        tabela.setStyle(TableStyle([
            # Cabeçalho moderno
            ('BACKGROUND', (0, 0), (-1, 0), self.cor_primaria),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            
            # Dados com zebra
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.cor_secundaria]),
            
            # Espaçamento e bordas
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.white),
        ]))
        
        return tabela
    
    def _criar_secao_feedback_ia_melhorada(self, feedback_ia):
        """Cria seção com feedback da IA"""
        elementos = []
        
        # Título da seção com design melhorado
        titulo_feedback = Paragraph(
            "🤖 FEEDBACK COMPORTAMENTAL PERSONALIZADO", 
            ParagraphStyle('FeedbackTitle', 
                         fontSize=18,
                         fontName='Helvetica-Bold',
                         textColor=self.cor_primaria,
                         spaceAfter=25,
                         spaceBefore=20,
                         alignment=1)
        )
        elementos.append(titulo_feedback)
        
        # Caixa de destaque para o feedback
        feedback_box_style = ParagraphStyle(
            'FeedbackBox',
            parent=self.corpo_style,
            fontSize=11,
            leading=16,
            spaceAfter=15,
            leftIndent=20,
            rightIndent=20,
            borderWidth=1,
            borderColor=self.cor_primaria,
            borderPadding=15,
            backColor=self.cor_secundaria
        )
        
        # Processar feedback em seções
        secoes = feedback_ia.split('\n\n')
        
        for i, secao in enumerate(secoes):
            if secao.strip():
                # Limpar emojis problemáticos
                secao_limpa = secao.replace('🤖', '').replace('📊', '').replace('⚠️', '').replace('💪', '').replace('🎯', '')
                
                # Identificar se é título de seção
                if any(palavra in secao_limpa.upper() for palavra in ['ANÁLISE', 'RECOMENDAÇÕES', 'PONTOS', 'PLANO']):
                    # É um título de seção
                    titulo_secao = Paragraph(
                        secao_limpa.strip(),
                        ParagraphStyle('SecaoTitle',
                                     fontSize=13,
                                     fontName='Helvetica-Bold', 
                                     textColor=self.cor_primaria,
                                     spaceAfter=10,
                                     spaceBefore=15)
                    )
                    elementos.append(titulo_secao)
                else:
                    # É conteúdo
                    paragrafo = Paragraph(secao_limpa.strip(), feedback_box_style)
                    elementos.append(paragrafo)
                    elementos.append(Spacer(1, 10))
        
        return elementos