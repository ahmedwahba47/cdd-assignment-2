#!/usr/bin/env python3
"""
PDF Report Generator for Container Design & Deployment Project #2
Student: Ahmed Wahba | ID: A00336722
Generates professional PDF report with colored diagrams, syntax highlighting, and proper formatting.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, ListFlowable, ListItem, Preformatted,
    KeepTogether, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics import renderPDF
import os
import re

# Configuration
STUDENT_NAME = "Ahmed Wahba"
STUDENT_ID = "A00336722"
ASSIGNMENT_NAME = "Container Design & Deployment Project #2 2025/26"
OUTPUT_FILE = "AhmedWahba_A00336722_CDD_Project2.pdf"
GIT_REPO_URL = "https://github.com/ahmedwahba47/cdd-assignment-2"

# Colors
HEADER_BLUE = colors.HexColor('#2C3E50')
ACCENT_BLUE = colors.HexColor('#3498DB')
LIGHT_GRAY = colors.HexColor('#F8F9FA')
CODE_BG = colors.HexColor('#282C34')  # Dark background for code
YAML_KEY = colors.HexColor('#E06C75')  # Red for YAML keys
YAML_VALUE = colors.HexColor('#98C379')  # Green for values
YAML_STRING = colors.HexColor('#E5C07B')  # Yellow for strings
CMD_BG = colors.HexColor('#1E1E1E')  # Darker for commands
CMD_PROMPT = colors.HexColor('#4EC9B0')  # Cyan for prompt
TABLE_HEADER = colors.HexColor('#34495E')
DOCKER_BLUE = colors.HexColor('#2496ED')
K8S_BLUE = colors.HexColor('#326CE5')
MYSQL_ORANGE = colors.HexColor('#F29111')
SPRING_GREEN = colors.HexColor('#6DB33F')
ELK_YELLOW = colors.HexColor('#FEC514')

# Figure counter
FIGURE_COUNT = [0]

def get_figure_number():
    FIGURE_COUNT[0] += 1
    return FIGURE_COUNT[0]


class NumberedCanvas(canvas.Canvas):
    """Canvas with page numbers"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber > 1:
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.gray)
            self.drawRightString(A4[0] - 1*cm, 1*cm, f"Page {self._pageNumber - 1} of {page_count - 1}")


def get_styles():
    """Create custom paragraph styles"""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='CoverTitle',
        fontSize=24,
        textColor=HEADER_BLUE,
        spaceAfter=30,
        spaceBefore=0,
        leading=32,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        fontSize=14,
        textColor=colors.gray,
        spaceAfter=10,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        name='SectionHeader',
        fontSize=18,
        textColor=HEADER_BLUE,
        spaceBefore=24,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='SubHeader',
        fontSize=14,
        textColor=HEADER_BLUE,
        spaceBefore=16,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='ReportBody',
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name='FigureCaption',
        fontSize=10,
        textColor=colors.HexColor('#444444'),
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=14,
        fontName='Helvetica-Oblique'
    ))

    styles.add(ParagraphStyle(
        name='TOCEntry',
        fontSize=11,
        leading=18,
        leftIndent=0
    ))

    styles.add(ParagraphStyle(
        name='TOCSubEntry',
        fontSize=10,
        leading=16,
        leftIndent=20,
        textColor=colors.HexColor('#555555')
    ))

    return styles


def create_docker_compose_diagram():
    """Create colored Docker Compose architecture diagram"""
    drawing = Drawing(480, 200)

    # Background
    drawing.add(Rect(0, 0, 480, 200, fillColor=colors.HexColor('#F5F5F5'), strokeColor=None))

    # Docker Network box
    drawing.add(Rect(20, 20, 440, 160, fillColor=colors.white, strokeColor=DOCKER_BLUE, strokeWidth=2))
    drawing.add(String(30, 165, "Docker Network (bookservice-network)", fontName='Helvetica-Bold', fontSize=10, fillColor=DOCKER_BLUE))

    # BookService container
    drawing.add(Rect(40, 60, 160, 90, fillColor=SPRING_GREEN, strokeColor=colors.HexColor('#5A9A30'), strokeWidth=2, rx=5, ry=5))
    drawing.add(String(70, 130, "BookService", fontName='Helvetica-Bold', fontSize=11, fillColor=colors.white))
    drawing.add(String(60, 115, "Spring Boot + Java 25", fontName='Helvetica', fontSize=8, fillColor=colors.white))
    drawing.add(String(90, 100, "Port: 8080", fontName='Helvetica', fontSize=8, fillColor=colors.white))
    drawing.add(String(75, 70, "REST API + JPA", fontName='Helvetica', fontSize=8, fillColor=colors.white))

    # Arrow
    drawing.add(Line(200, 105, 260, 105, strokeColor=colors.HexColor('#666666'), strokeWidth=2))
    drawing.add(Polygon([260, 105, 250, 110, 250, 100], fillColor=colors.HexColor('#666666'), strokeColor=None))

    # MySQL container
    drawing.add(Rect(280, 60, 160, 90, fillColor=MYSQL_ORANGE, strokeColor=colors.HexColor('#D4820F'), strokeWidth=2, rx=5, ry=5))
    drawing.add(String(330, 130, "MySQL 8.4", fontName='Helvetica-Bold', fontSize=11, fillColor=colors.white))
    drawing.add(String(320, 115, "Database Server", fontName='Helvetica', fontSize=8, fillColor=colors.white))
    drawing.add(String(330, 100, "Port: 3306", fontName='Helvetica', fontSize=8, fillColor=colors.white))
    drawing.add(String(325, 70, "bookdb schema", fontName='Helvetica', fontSize=8, fillColor=colors.white))

    # Volumes
    drawing.add(Rect(60, 25, 80, 25, fillColor=colors.HexColor('#95A5A6'), strokeColor=None, rx=3, ry=3))
    drawing.add(String(70, 33, "app_logs", fontName='Helvetica', fontSize=8, fillColor=colors.white))

    drawing.add(Rect(320, 25, 80, 25, fillColor=colors.HexColor('#95A5A6'), strokeColor=None, rx=3, ry=3))
    drawing.add(String(325, 33, "mysql_data", fontName='Helvetica', fontSize=8, fillColor=colors.white))

    return drawing


def create_swarm_diagram():
    """Create Docker Swarm architecture diagram"""
    drawing = Drawing(480, 240)

    # Background
    drawing.add(Rect(0, 0, 480, 240, fillColor=colors.HexColor('#F0F4F8'), strokeColor=None))

    # Swarm cluster border
    drawing.add(Rect(10, 10, 460, 220, fillColor=None, strokeColor=DOCKER_BLUE, strokeWidth=2, strokeDashArray=[5, 3]))
    drawing.add(String(180, 215, "Docker Swarm Cluster", fontName='Helvetica-Bold', fontSize=12, fillColor=DOCKER_BLUE))

    # Manager Node (scheduling and orchestration only)
    drawing.add(Rect(20, 140, 100, 60, fillColor=colors.HexColor('#27AE60'), strokeColor=colors.HexColor('#1E8449'), strokeWidth=2, rx=5, ry=5))
    drawing.add(String(35, 185, "Manager Node", fontName='Helvetica-Bold', fontSize=8, fillColor=colors.white))
    drawing.add(String(30, 165, "Orchestration", fontName='Helvetica', fontSize=7, fillColor=colors.white))
    drawing.add(String(35, 150, "Scheduling", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    # Worker nodes with services
    # Worker 1 - bookservice replica 1
    drawing.add(Rect(140, 140, 100, 60, fillColor=colors.HexColor('#3498DB'), strokeColor=colors.HexColor('#2980B9'), strokeWidth=2, rx=5, ry=5))
    drawing.add(String(155, 185, "Worker Node 1", fontName='Helvetica-Bold', fontSize=8, fillColor=colors.white))
    drawing.add(Rect(150, 150, 80, 25, fillColor=SPRING_GREEN, strokeColor=None, rx=3, ry=3))
    drawing.add(String(160, 157, "bookservice:1", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    # Worker 2 - bookservice replica 2
    drawing.add(Rect(260, 140, 100, 60, fillColor=colors.HexColor('#3498DB'), strokeColor=colors.HexColor('#2980B9'), strokeWidth=2, rx=5, ry=5))
    drawing.add(String(275, 185, "Worker Node 2", fontName='Helvetica-Bold', fontSize=8, fillColor=colors.white))
    drawing.add(Rect(270, 150, 80, 25, fillColor=SPRING_GREEN, strokeColor=None, rx=3, ry=3))
    drawing.add(String(280, 157, "bookservice:2", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    # Worker 3 - MySQL (stateful, pinned to one node)
    drawing.add(Rect(380, 140, 80, 60, fillColor=colors.HexColor('#3498DB'), strokeColor=colors.HexColor('#2980B9'), strokeWidth=2, rx=5, ry=5))
    drawing.add(String(390, 185, "Worker Node 3", fontName='Helvetica-Bold', fontSize=8, fillColor=colors.white))
    drawing.add(Rect(390, 150, 60, 25, fillColor=MYSQL_ORANGE, strokeColor=None, rx=3, ry=3))
    drawing.add(String(400, 157, "MySQL", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    # Overlay network line
    drawing.add(Line(20, 130, 460, 130, strokeColor=colors.HexColor('#9B59B6'), strokeWidth=2))
    drawing.add(String(180, 115, "Overlay Network", fontName='Helvetica-Bold', fontSize=9, fillColor=colors.HexColor('#9B59B6')))

    # Ingress load balancer
    drawing.add(Rect(150, 60, 180, 40, fillColor=colors.HexColor('#E74C3C'), strokeColor=None, rx=5, ry=5))
    drawing.add(String(175, 80, "Ingress Load Balancer", fontName='Helvetica-Bold', fontSize=9, fillColor=colors.white))
    drawing.add(String(210, 65, ":8080", fontName='Helvetica', fontSize=8, fillColor=colors.white))

    # Persistent Volume for MySQL
    drawing.add(Rect(385, 20, 70, 30, fillColor=colors.HexColor('#95A5A6'), strokeColor=None, rx=3, ry=3))
    drawing.add(String(395, 30, "Volume", fontName='Helvetica', fontSize=7, fillColor=colors.white))
    drawing.add(Line(420, 50, 420, 140, strokeColor=colors.HexColor('#95A5A6'), strokeWidth=1, strokeDashArray=[2,2]))

    return drawing


def create_kubernetes_diagram():
    """Create Kubernetes architecture diagram"""
    drawing = Drawing(460, 280)

    # Background
    drawing.add(Rect(0, 0, 460, 280, fillColor=colors.HexColor('#F8F9FA'), strokeColor=None))

    # Cluster border
    drawing.add(Rect(10, 10, 440, 260, fillColor=None, strokeColor=K8S_BLUE, strokeWidth=2))
    drawing.add(String(160, 255, "Kubernetes Cluster", fontName='Helvetica-Bold', fontSize=12, fillColor=K8S_BLUE))

    # Namespace box
    drawing.add(Rect(20, 20, 420, 225, fillColor=colors.HexColor('#E8F4FD'), strokeColor=K8S_BLUE, strokeWidth=1, strokeDashArray=[3, 2]))
    drawing.add(String(25, 230, "Namespace: bookservice", fontName='Helvetica-Bold', fontSize=9, fillColor=K8S_BLUE))

    # ConfigMap, Secret, PVC - centered at top (total width ~200, centered in 420 = start at 110)
    drawing.add(Rect(110, 190, 70, 28, fillColor=colors.HexColor('#9B59B6'), strokeColor=None, rx=3, ry=3))
    drawing.add(String(123, 200, "ConfigMap", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    drawing.add(Rect(195, 190, 60, 28, fillColor=colors.HexColor('#E74C3C'), strokeColor=None, rx=3, ry=3))
    drawing.add(String(212, 200, "Secret", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    drawing.add(Rect(270, 190, 50, 28, fillColor=colors.HexColor('#95A5A6'), strokeColor=None, rx=3, ry=3))
    drawing.add(String(286, 200, "PVC", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    # MySQL Deployment - centered (width 180, centered in 420 = start at 120)
    drawing.add(Rect(120, 120, 180, 55, fillColor=colors.white, strokeColor=MYSQL_ORANGE, strokeWidth=2, rx=5, ry=5))
    drawing.add(String(155, 160, "MySQL Deployment", fontName='Helvetica-Bold', fontSize=8, fillColor=MYSQL_ORANGE))
    drawing.add(Rect(135, 130, 50, 22, fillColor=MYSQL_ORANGE, strokeColor=None, rx=3, ry=3))
    drawing.add(String(152, 137, "Pod", fontName='Helvetica', fontSize=7, fillColor=colors.white))
    drawing.add(Rect(200, 130, 80, 22, fillColor=colors.HexColor('#16A085'), strokeColor=None, rx=3, ry=3))
    drawing.add(String(215, 137, "ClusterIP Svc", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    # BookService Deployment - centered (width 290, centered in 420 = start at 65)
    drawing.add(Rect(30, 40, 290, 65, fillColor=colors.white, strokeColor=SPRING_GREEN, strokeWidth=2, rx=5, ry=5))
    drawing.add(String(75, 90, "BookService Deployment (3 replicas)", fontName='Helvetica-Bold', fontSize=8, fillColor=SPRING_GREEN))
    drawing.add(Rect(45, 50, 48, 28, fillColor=SPRING_GREEN, strokeColor=None, rx=3, ry=3))
    drawing.add(String(57, 60, "Pod 1", fontName='Helvetica', fontSize=7, fillColor=colors.white))
    drawing.add(Rect(103, 50, 48, 28, fillColor=SPRING_GREEN, strokeColor=None, rx=3, ry=3))
    drawing.add(String(115, 60, "Pod 2", fontName='Helvetica', fontSize=7, fillColor=colors.white))
    drawing.add(Rect(161, 50, 48, 28, fillColor=SPRING_GREEN, strokeColor=None, rx=3, ry=3))
    drawing.add(String(173, 60, "Pod 3", fontName='Helvetica', fontSize=7, fillColor=colors.white))
    drawing.add(Rect(220, 50, 85, 28, fillColor=colors.HexColor('#2980B9'), strokeColor=None, rx=3, ry=3))
    drawing.add(String(232, 60, "NodePort:30080", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    # HPA - with margin from edge
    drawing.add(Rect(340, 50, 85, 55, fillColor=colors.HexColor('#F39C12'), strokeColor=None, rx=5, ry=5))
    drawing.add(String(370, 90, "HPA", fontName='Helvetica-Bold', fontSize=9, fillColor=colors.white))
    drawing.add(String(360, 73, "min: 2", fontName='Helvetica', fontSize=8, fillColor=colors.white))
    drawing.add(String(360, 58, "max: 10", fontName='Helvetica', fontSize=8, fillColor=colors.white))

    return drawing


def create_elk_diagram():
    """Create ELK Stack diagram"""
    drawing = Drawing(460, 160)

    # Background - reduced width
    drawing.add(Rect(0, 0, 460, 160, fillColor=colors.HexColor('#FFF9E6'), strokeColor=None))

    # App logs
    drawing.add(Rect(15, 55, 70, 50, fillColor=SPRING_GREEN, strokeColor=None, rx=5, ry=5))
    drawing.add(String(22, 80, "BookService", fontName='Helvetica-Bold', fontSize=8, fillColor=colors.white))
    drawing.add(String(30, 65, "test.log", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    # Arrow to Logstash
    drawing.add(Line(85, 80, 115, 80, strokeColor=colors.gray, strokeWidth=2))
    drawing.add(Polygon([115, 80, 107, 85, 107, 75], fillColor=colors.gray))

    # Logstash
    drawing.add(Rect(120, 45, 85, 70, fillColor=ELK_YELLOW, strokeColor=None, rx=5, ry=5))
    drawing.add(String(135, 95, "Logstash", fontName='Helvetica-Bold', fontSize=9, fillColor=colors.HexColor('#333')))
    drawing.add(String(125, 80, "Parse & Filter", fontName='Helvetica', fontSize=7, fillColor=colors.HexColor('#333')))
    drawing.add(String(130, 55, "Grok Pattern", fontName='Helvetica', fontSize=7, fillColor=colors.HexColor('#666')))

    # Arrow to Elasticsearch
    drawing.add(Line(205, 80, 235, 80, strokeColor=colors.gray, strokeWidth=2))
    drawing.add(Polygon([235, 80, 227, 85, 227, 75], fillColor=colors.gray))

    # Elasticsearch
    drawing.add(Rect(240, 45, 90, 70, fillColor=colors.HexColor('#00BFB3'), strokeColor=None, rx=5, ry=5))
    drawing.add(String(248, 95, "Elasticsearch", fontName='Helvetica-Bold', fontSize=9, fillColor=colors.white))
    drawing.add(String(255, 80, "Index & Store", fontName='Helvetica', fontSize=7, fillColor=colors.white))
    drawing.add(String(270, 55, ":9200", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    # Arrow to Kibana
    drawing.add(Line(330, 80, 360, 80, strokeColor=colors.gray, strokeWidth=2))
    drawing.add(Polygon([360, 80, 352, 85, 352, 75], fillColor=colors.gray))

    # Kibana - now fits inside
    drawing.add(Rect(365, 45, 80, 70, fillColor=colors.HexColor('#E8478B'), strokeColor=None, rx=5, ry=5))
    drawing.add(String(385, 95, "Kibana", fontName='Helvetica-Bold', fontSize=9, fillColor=colors.white))
    drawing.add(String(380, 80, "Visualize", fontName='Helvetica', fontSize=7, fillColor=colors.white))
    drawing.add(String(393, 55, ":5601", fontName='Helvetica', fontSize=7, fillColor=colors.white))

    # Title
    drawing.add(String(160, 135, "ELK Stack Data Flow", fontName='Helvetica-Bold', fontSize=11, fillColor=colors.HexColor('#333')))

    return drawing


def create_comparison_chart():
    """Create orchestration tools comparison bar chart"""
    drawing = Drawing(450, 240)

    chart = VerticalBarChart()
    chart.x = 60
    chart.y = 90
    chart.height = 120
    chart.width = 340

    # Data: [Setup Complexity, Learning Curve, Scalability, Feature Set]
    chart.data = [
        [1, 1, 1, 2],    # Docker Compose
        [2, 2, 3, 3],    # Docker Swarm
        [4, 4, 5, 5],    # Kubernetes
    ]

    chart.categoryAxis.categoryNames = ['Setup', 'Learning', 'Scalability', 'Features']
    chart.categoryAxis.labels.fontSize = 8
    chart.categoryAxis.labels.boxAnchor = 'n'
    chart.categoryAxis.labels.dy = -3

    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 5
    chart.valueAxis.valueStep = 1
    chart.valueAxis.labels.fontSize = 8

    chart.bars[0].fillColor = DOCKER_BLUE
    chart.bars[1].fillColor = colors.HexColor('#2ECC71')
    chart.bars[2].fillColor = K8S_BLUE

    chart.barWidth = 14
    chart.groupSpacing = 25

    drawing.add(chart)

    # Legend - positioned at bottom, horizontally centered
    legend = Legend()
    legend.x = 80
    legend.y = 20
    legend.dx = 10
    legend.dy = 10
    legend.fontName = 'Helvetica'
    legend.fontSize = 9
    legend.boxAnchor = 'sw'
    legend.columnMaximum = 3
    legend.strokeWidth = 0.5
    legend.strokeColor = colors.black
    legend.deltax = 130
    legend.deltay = 0
    legend.autoXPadding = 15
    legend.colorNamePairs = [
        (DOCKER_BLUE, 'Docker Compose'),
        (colors.HexColor('#2ECC71'), 'Docker Swarm'),
        (K8S_BLUE, 'Kubernetes'),
    ]
    drawing.add(legend)

    return drawing


def create_styled_code_block(code, lang='yaml'):
    """Create a styled code block with syntax highlighting simulation"""
    # We'll create a table with dark background containing formatted code
    lines = code.strip().split('\n')

    # Wrap long lines to prevent overflow
    max_chars = 70
    wrapped_lines = []
    for line in lines:
        if len(line) > max_chars:
            # Break long lines
            while len(line) > max_chars:
                wrapped_lines.append(line[:max_chars])
                line = '  ' + line[max_chars:]  # indent continuation
            if line.strip():
                wrapped_lines.append(line)
        else:
            wrapped_lines.append(line)

    data = []
    for line in wrapped_lines:
        data.append([line])

    if not data:
        data = [['# empty']]

    table = Table(data, colWidths=[5.8*inch])

    style = [
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#ABB2BF')),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]

    # Round corners effect with box
    style.append(('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3E4451')))

    table.setStyle(TableStyle(style))
    return table


def create_command_block(cmd):
    """Create a styled command block"""
    lines = cmd.strip().split('\n')

    data = []
    for line in lines:
        if line.startswith('#'):
            data.append([line])
        else:
            data.append(['$ ' + line if line and not line.startswith('$') else line])

    table = Table(data, colWidths=[6*inch])

    style = [
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, -1), CMD_BG),
        ('TEXTCOLOR', (0, 0), (-1, -1), CMD_PROMPT),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3E4451')),
    ]

    table.setStyle(TableStyle(style))
    return table


def create_table(data, col_widths=None, header=True):
    """Create styled table"""
    if col_widths is None:
        col_widths = [2*inch] * len(data[0])

    table = Table(data, colWidths=col_widths)

    style = [
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DEE2E6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]

    if header:
        style.extend([
            ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ])
        for i in range(1, len(data)):
            if i % 2 == 0:
                style.append(('BACKGROUND', (0, i), (-1, i), LIGHT_GRAY))

    table.setStyle(TableStyle(style))
    return table


def build_cover_page(styles):
    """Build cover page"""
    elements = []
    elements.append(Spacer(1, 1.5*inch))

    elements.append(Paragraph(ASSIGNMENT_NAME, styles['CoverTitle']))
    elements.append(Spacer(1, 0.3*inch))

    elements.append(Paragraph("Book Management Microservice", styles['CoverSubtitle']))
    elements.append(Paragraph("Docker Compose | Docker Swarm | Kubernetes", styles['CoverSubtitle']))

    elements.append(Spacer(1, 1.2*inch))

    info_data = [
        ['Student Name:', STUDENT_NAME],
        ['Student ID:', STUDENT_ID],
        ['Module:', 'Container Design & Deployment'],
        ['Submission Date:', 'December 2025'],
    ]
    if GIT_REPO_URL:
        info_data.append(['Repository:', GIT_REPO_URL])

    info_table = Table(info_data, colWidths=[1.6*inch, 3.2*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    elements.append(info_table)

    elements.append(PageBreak())
    return elements


def build_toc(styles):
    """Build properly formatted table of contents"""
    elements = []
    elements.append(Paragraph("Table of Contents", styles['SectionHeader']))
    elements.append(Spacer(1, 0.3*inch))

    toc_data = [
        ("1. Introduction", "3", False),
        ("1.1 Microservices and Containerisation", "3", True),
        ("1.2 Container Orchestration", "4", True),
        ("1.3 Logging and Monitoring", "4", True),
        ("2. Docker Compose Deployment", "5", False),
        ("2.1 Overview and Features", "5", True),
        ("2.2 Microservice Architecture", "5", True),
        ("2.3 Dockerfile Design", "6", True),
        ("2.4 Deployment Steps", "7", True),
        ("2.5 ELK Stack Integration", "8", True),
        ("3. Docker Swarm Deployment", "9", False),
        ("3.1 Swarm Architecture", "9", True),
        ("3.2 Stack Configuration", "10", True),
        ("3.3 Scaling and Rollback", "10", True),
        ("4. Kubernetes Deployment", "11", False),
        ("4.1 Core Components", "11", True),
        ("4.2 Architecture and Configuration", "12", True),
        ("4.3 Helm Charts", "13", True),
        ("5. Evaluation and Conclusion", "14", False),
        ("6. AI Assistance Acknowledgment", "15", False),
    ]

    toc_table_data = []
    for title, page, is_sub in toc_data:
        if is_sub:
            toc_table_data.append([f"    {title}", page])
        else:
            toc_table_data.append([title, page])

    toc_table = Table(toc_table_data, colWidths=[5*inch, 0.5*inch])
    toc_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#EEEEEE')),
    ]))

    # Make main sections bold
    for i, (_, _, is_sub) in enumerate(toc_data):
        if not is_sub:
            toc_table.setStyle(TableStyle([('FONTNAME', (0, i), (0, i), 'Helvetica-Bold')]))

    elements.append(toc_table)
    elements.append(PageBreak())
    return elements


def build_introduction(styles):
    """Build introduction section"""
    elements = []

    elements.append(Paragraph("1. Introduction", styles['SectionHeader']))

    elements.append(Paragraph("1.1 Microservices and Containerisation", styles['SubHeader']))

    elements.append(Paragraph(
        "<b>Microservices architecture</b> structures applications as a collection of loosely coupled, "
        "independently deployable services. Each service handles a specific business capability, "
        "can be deployed without affecting others, and may use different technology stacks.",
        styles['ReportBody']
    ))

    elements.append(Paragraph(
        "<b>Containerisation</b> packages applications with their dependencies into isolated, portable "
        "units. Key benefits include:",
        styles['ReportBody']
    ))

    container_benefits = [
        ['Benefit', 'Description'],
        ['Consistency', 'Identical environment from development to production'],
        ['Isolation', 'Applications run without conflicts with other processes'],
        ['Portability', 'Runs on any platform supporting container runtime'],
        ['Efficiency', 'Lightweight compared to VMs (shared OS kernel)'],
        ['Speed', 'Containers start in seconds, enabling rapid deployment'],
    ]
    elements.append(create_table(container_benefits, [1.2*inch, 4.5*inch]))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph(
        "In this project, I developed a <b>Book Management Microservice</b> using Java Spring Boot (Java 25 LTS)"
        "that provides RESTful APIs for CRUD operations on a book inventory, backed by MySQL 8.4.",
        styles['ReportBody']
    ))

    elements.append(Paragraph("1.2 The Role of Container Orchestration", styles['SubHeader']))

    elements.append(Paragraph(
        "Container orchestration automates deployment, scaling, and management of containerised "
        "applications. As microservice architectures grow, orchestration provides:",
        styles['ReportBody']
    ))

    orchestration_features = [
        ['Function', 'Description'],
        ['Scheduling', 'Assigns containers to nodes based on resource availability'],
        ['Service Discovery', 'Enables containers to find each other dynamically'],
        ['Load Balancing', 'Distributes traffic across container instances'],
        ['Scaling', 'Adjusts container count based on demand'],
        ['Self-healing', 'Replaces failed containers automatically'],
        ['Rolling Updates', 'Deploys updates without service downtime'],
    ]
    elements.append(create_table(orchestration_features, [1.3*inch, 4.4*inch]))

    elements.append(PageBreak())

    elements.append(Paragraph("1.3 Logging and Monitoring in Distributed Systems", styles['SubHeader']))

    elements.append(Paragraph(
        "Observability is critical in microservice systems. The <b>ELK Stack</b> provides comprehensive logging:",
        styles['ReportBody']
    ))

    elk_table = [
        ['Component', 'Role'],
        ['Elasticsearch', 'Distributed search engine for storing and querying logs'],
        ['Logstash', 'Pipeline for collecting, parsing, and forwarding logs'],
        ['Kibana', 'Dashboard for visualising and analysing log data'],
    ]
    elements.append(create_table(elk_table, [1.3*inch, 4.4*inch]))

    elements.append(PageBreak())
    return elements


def build_docker_compose_section(styles):
    """Build Docker Compose section with diagrams"""
    elements = []

    elements.append(Paragraph("2. Docker Compose Deployment", styles['SectionHeader']))

    elements.append(Paragraph("2.1 What is Docker Compose?", styles['SubHeader']))

    elements.append(Paragraph(
        "Docker Compose is a tool for defining and running multi-container applications using "
        "declarative YAML configuration.",
        styles['ReportBody']
    ))

    compose_features = [
        ['Feature', 'Description'],
        ['Declarative Config', 'Services, networks, volumes defined in YAML'],
        ['Dependency Management', 'Control startup order with depends_on'],
        ['Environment Variables', 'Configuration via .env files'],
        ['Volume Persistence', 'Data persists across container restarts'],
        ['Network Isolation', 'Services communicate via custom networks'],
    ]
    elements.append(create_table(compose_features, [1.5*inch, 4.2*inch]))

    elements.append(Paragraph("2.2 Microservice Architecture", styles['SubHeader']))

    elements.append(Paragraph(
        "The Book Management application consists of two containers communicating over a bridge network:",
        styles['ReportBody']
    ))

    # Add colored diagram
    fig_num = get_figure_number()
    elements.append(create_docker_compose_diagram())
    elements.append(Paragraph(f"Figure {fig_num}: Docker Compose Architecture - BookService and MySQL containers", styles['FigureCaption']))

    elements.append(Paragraph("2.3 Dockerfile (Multi-stage Build)", styles['SubHeader']))

    elements.append(Paragraph(
        "The Dockerfile uses multi-stage build to optimise the image size:",
        styles['ReportBody']
    ))

    dockerfile_code = """# Stage 1: Build
FROM maven:3.9-eclipse-temurin-25 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:25-jre-alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
USER appuser
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s CMD wget -q --spider http://localhost:8080/actuator/health
ENTRYPOINT ["java", "-jar", "app.jar"]"""

    elements.append(create_styled_code_block(dockerfile_code, 'dockerfile'))
    fig_num = get_figure_number()
    elements.append(Paragraph(f"Figure {fig_num}: Multi-stage Dockerfile for BookService", styles['FigureCaption']))

    elements.append(Paragraph("2.4 Deployment Steps", styles['SubHeader']))

    elements.append(Paragraph("<b>Build and Start Services:</b>", styles['ReportBody']))
    elements.append(create_command_block("cd docker-compose\ndocker-compose up -d --build"))

    elements.append(Paragraph("<b>Verify Containers:</b>", styles['ReportBody']))
    elements.append(create_command_block("docker-compose ps\ndocker-compose logs -f bookservice"))

    elements.append(Paragraph("<b>Test API Endpoints:</b>", styles['ReportBody']))
    api_endpoints = [
        ['Method', 'Endpoint', 'Description'],
        ['GET', '/api/books', 'Retrieve all books'],
        ['GET', '/api/books/{id}', 'Get book by ID'],
        ['POST', '/api/books', 'Create new book'],
        ['PUT', '/api/books/{id}', 'Update book'],
        ['DELETE', '/api/books/{id}', 'Delete book'],
        ['GET', '/actuator/health', 'Health check'],
    ]
    elements.append(create_table(api_endpoints, [0.8*inch, 1.6*inch, 2.5*inch]))

    elements.append(Paragraph("<b>Push to Docker Hub:</b>", styles['ReportBody']))
    elements.append(create_command_block("docker login\ndocker tag bookservice:1.0.0 ahmedwahba/bookservice:1.0.0\ndocker push ahmedwahba/bookservice:1.0.0"))

    elements.append(Paragraph("2.5 ELK Stack Integration", styles['SubHeader']))

    fig_num = get_figure_number()
    elements.append(create_elk_diagram())
    elements.append(Paragraph(f"Figure {fig_num}: ELK Stack Data Flow for Log Processing", styles['FigureCaption']))

    elements.append(Paragraph("<b>Logstash Configuration:</b>", styles['ReportBody']))
    logstash_conf = """input {
  file {
    path => "/app/logs/test.log"
    start_position => "beginning"
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} | %{WORD:method} %{URIPATH:endpoint}" }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "bookservice-logs-%{+YYYY.MM.dd}"
  }
}"""
    elements.append(create_styled_code_block(logstash_conf, 'conf'))

    elements.append(PageBreak())
    return elements


def build_docker_swarm_section(styles):
    """Build Docker Swarm section"""
    elements = []

    elements.append(Paragraph("3. Docker Swarm Deployment", styles['SectionHeader']))

    elements.append(Paragraph("3.1 What is Docker Swarm?", styles['SubHeader']))

    elements.append(Paragraph(
        "Docker Swarm is Docker's native clustering and orchestration tool.",
        styles['ReportBody']
    ))

    swarm_components = [
        ['Component', 'Description'],
        ['Manager Nodes', 'Control cluster state, schedule services'],
        ['Worker Nodes', 'Execute container tasks'],
        ['Services', 'Declarative definition of desired state'],
        ['Tasks', 'Individual container instances'],
        ['Overlay Network', 'Multi-host networking'],
        ['Ingress', 'Built-in load balancing'],
    ]
    elements.append(create_table(swarm_components, [1.3*inch, 4.4*inch]))

    elements.append(Paragraph("3.2 Swarm Architecture", styles['SubHeader']))

    fig_num = get_figure_number()
    elements.append(create_swarm_diagram())
    elements.append(Paragraph(f"Figure {fig_num}: Docker Swarm Cluster with Manager and Worker Nodes", styles['FigureCaption']))

    elements.append(Paragraph("3.3 Stack Configuration", styles['SubHeader']))

    stack_yaml = """version: '3.8'
services:
  bookservice:
    image: ahmedwahba/bookservice:1.0.0
    deploy:
      mode: replicated
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    networks:
      - bookservice-network

networks:
  bookservice-network:
    driver: overlay"""
    elements.append(create_styled_code_block(stack_yaml, 'yaml'))
    fig_num = get_figure_number()
    elements.append(Paragraph(f"Figure {fig_num}: Docker Stack YAML Configuration", styles['FigureCaption']))

    elements.append(Paragraph("3.4 Deployment and Scaling", styles['SubHeader']))

    elements.append(Paragraph("<b>Initialize and Deploy:</b>", styles['ReportBody']))
    elements.append(create_command_block("docker swarm init\ndocker stack deploy -c docker-stack.yml bookservice-stack"))

    elements.append(Paragraph("<b>Scale Services:</b>", styles['ReportBody']))
    elements.append(create_command_block("docker service scale bookservice-stack_bookservice=5"))

    elements.append(Paragraph("<b>Rolling Update and Rollback:</b>", styles['ReportBody']))
    elements.append(create_command_block("docker service update \\\n  --image ahmedwahba/bookservice:2.0.0 \\\n  bookservice-stack_bookservice\ndocker service rollback bookservice-stack_bookservice"))

    elements.append(Paragraph("3.5 Advantages and Limitations", styles['SubHeader']))

    swarm_comparison = [
        ['Advantages', 'Limitations'],
        ['Native Docker integration', 'Smaller ecosystem than K8s'],
        ['Simple setup', 'No built-in auto-scaling'],
        ['Low learning curve', 'Limited networking options'],
        ['Built-in load balancing', 'Fewer integrations'],
    ]
    elements.append(create_table(swarm_comparison, [2.8*inch, 2.8*inch]))

    elements.append(PageBreak())
    return elements


def build_kubernetes_section(styles):
    """Build Kubernetes section"""
    elements = []

    elements.append(Paragraph("4. Kubernetes Deployment", styles['SectionHeader']))

    elements.append(Paragraph("4.1 What is Kubernetes?", styles['SubHeader']))

    elements.append(Paragraph(
        "Kubernetes (K8s) is an open-source container orchestration platform providing automated "
        "deployment, scaling, and management of containerised applications.",
        styles['ReportBody']
    ))

    k8s_components = [
        ['Component', 'Description'],
        ['Pod', 'Smallest deployable unit; containers sharing network'],
        ['Deployment', 'Manages ReplicaSets and declarative updates'],
        ['Service', 'Stable network endpoint for pods'],
        ['ConfigMap', 'Non-sensitive configuration data'],
        ['Secret', 'Sensitive data (passwords, tokens)'],
        ['PVC', 'Persistent storage request'],
        ['HPA', 'Automatic scaling based on metrics'],
    ]
    elements.append(create_table(k8s_components, [1.2*inch, 4.5*inch]))

    elements.append(Paragraph("4.2 Architecture", styles['SubHeader']))

    fig_num = get_figure_number()
    elements.append(create_kubernetes_diagram())
    elements.append(Paragraph(f"Figure {fig_num}: Kubernetes Cluster Architecture with HPA", styles['FigureCaption']))

    elements.append(Paragraph("4.3 Deployment Configuration", styles['SubHeader']))

    k8s_yaml = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: bookservice
  namespace: bookservice
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    spec:
      containers:
        - name: bookservice
          image: ahmedwahba/bookservice:1.0.0
          resources:
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /actuator/health
              port: 8080"""
    elements.append(create_styled_code_block(k8s_yaml, 'yaml'))
    fig_num = get_figure_number()
    elements.append(Paragraph(f"Figure {fig_num}: Kubernetes Deployment Manifest", styles['FigureCaption']))

    elements.append(Paragraph("<b>Deploy and Scale:</b>", styles['ReportBody']))
    elements.append(create_command_block("kubectl apply -k .\nkubectl scale deployment bookservice -n bookservice --replicas=5\nkubectl rollout undo deployment/bookservice -n bookservice"))

    elements.append(Paragraph("4.4 Helm Charts", styles['SubHeader']))

    elements.append(Paragraph(
        "Helm is the package manager for Kubernetes, enabling templated deployments:",
        styles['ReportBody']
    ))

    elements.append(create_command_block("helm install bookservice ./bookservice-chart -n bookservice\nhelm upgrade bookservice ./bookservice-chart --set replicaCount=5\nhelm rollback bookservice -n bookservice"))

    helm_benefits = ListFlowable([
        ListItem(Paragraph("Templating - Parameterised configs for environments", styles['ReportBody'])),
        ListItem(Paragraph("Versioning - Track deployment versions", styles['ReportBody'])),
        ListItem(Paragraph("Dependencies - Manage chart dependencies", styles['ReportBody'])),
        ListItem(Paragraph("Rollbacks - Easy rollback to previous release", styles['ReportBody'])),
    ], bulletType='bullet')
    elements.append(helm_benefits)

    elements.append(PageBreak())
    return elements


def build_evaluation_section(styles):
    """Build evaluation section"""
    elements = []

    elements.append(Paragraph("5. Evaluation and Conclusion", styles['SectionHeader']))

    elements.append(Paragraph("5.1 Comparative Analysis", styles['SubHeader']))

    fig_num = get_figure_number()
    elements.append(create_comparison_chart())
    elements.append(Paragraph(f"Figure {fig_num}: Orchestration Tools Comparison (1=Low, 5=High)", styles['FigureCaption']))

    comparison_table = [
        ['Feature', 'Docker Compose', 'Docker Swarm', 'Kubernetes'],
        ['Setup', 'Low', 'Medium', 'High'],
        ['Learning Curve', 'Easy', 'Moderate', 'Steep'],
        ['Scalability', 'Single host', 'Multi-host', 'Enterprise'],
        ['Auto-scaling', 'No', 'No', 'Yes (HPA)'],
        ['Rolling Updates', 'Basic', 'Yes', 'Advanced'],
        ['Best For', 'Development', 'Small prod', 'Enterprise'],
    ]
    elements.append(create_table(comparison_table, [1.1*inch, 1.2*inch, 1.2*inch, 1.4*inch]))

    elements.append(Paragraph("5.2 Reflection", styles['SubHeader']))

    elements.append(Paragraph("<b>What Worked Well:</b>", styles['ReportBody']))
    worked = ListFlowable([
        ListItem(Paragraph("Docker Compose enabled quick local iteration - I could rebuild and test changes in seconds", styles['ReportBody'])),
        ListItem(Paragraph("Multi-stage Dockerfile reduced image size from ~800MB to ~350MB (over 50% reduction)", styles['ReportBody'])),
        ListItem(Paragraph("Health checks with depends_on condition ensured MySQL was ready before the app started", styles['ReportBody'])),
        ListItem(Paragraph("Helm charts made it easy to deploy the same app with different configurations", styles['ReportBody'])),
        ListItem(Paragraph("Using non-root user in containers improved security posture", styles['ReportBody'])),
    ], bulletType='bullet')
    elements.append(worked)

    elements.append(Paragraph("<b>Challenges and Solutions:</b>", styles['ReportBody']))
    challenges = ListFlowable([
        ListItem(Paragraph("MySQL startup timing - initially the app crashed when MySQL wasn't ready. Solved by adding health checks and depends_on with condition: service_healthy", styles['ReportBody'])),
        ListItem(Paragraph("Kubernetes networking - understanding Services, ClusterIP vs NodePort took time. Reading official docs and hands-on practice helped", styles['ReportBody'])),
        ListItem(Paragraph("Minikube image caching - K8s kept using old container images. Solved by changing the image tag (1.0.0 to 1.0.1) to force a fresh pull", styles['ReportBody'])),
        ListItem(Paragraph("Port conflicts - running all 3 orchestrators simultaneously required different ports. Configured Compose on 8080, Swarm on 8081, and K8s on 30080", styles['ReportBody'])),
    ], bulletType='bullet')
    elements.append(challenges)

    elements.append(Paragraph("<b>Key Learnings:</b>", styles['ReportBody']))
    learnings = ListFlowable([
        ListItem(Paragraph("Infrastructure as Code is powerful - all configs in version control means reproducible deployments", styles['ReportBody'])),
        ListItem(Paragraph("Start simple, add complexity as needed - Compose for dev, K8s for production", styles['ReportBody'])),
        ListItem(Paragraph("Observability is not optional - without logs, debugging distributed systems is nearly impossible", styles['ReportBody'])),
    ], bulletType='bullet')
    elements.append(learnings)

    elements.append(Paragraph("5.3 Conclusion", styles['SubHeader']))

    elements.append(Paragraph(
        "This project gave me hands-on experience with container orchestration at three different levels. "
        "I built a complete microservice from scratch with Spring Boot, containerised it with Docker, "
        "and deployed it using three orchestration tools.",
        styles['ReportBody']
    ))

    elements.append(Paragraph(
        "<b>Docker Compose</b> is my choice for local development. It's simple, fast, and matches how I think "
        "about multi-container applications. The YAML syntax is intuitive, and I can go from code change to "
        "running container in under a minute.",
        styles['ReportBody']
    ))

    elements.append(Paragraph(
        "<b>Docker Swarm</b> surprised me with its simplicity. For smaller production deployments where you need "
        "scaling and high availability but don't want the complexity of Kubernetes, Swarm is a solid choice. "
        "The transition from Compose to Swarm is nearly seamless.",
        styles['ReportBody']
    ))

    elements.append(Paragraph(
        "<b>Kubernetes</b> is clearly the most powerful option. Features like HPA (auto-scaling), rolling updates "
        "with zero downtime, and declarative configuration make it ideal for enterprise production. The learning "
        "curve is steep, but the payoff is worth it for complex systems.",
        styles['ReportBody']
    ))

    elements.append(Paragraph(
        "<b>Production Recommendation:</b> For a real production system, I would use Docker Compose during development "
        "and Kubernetes for deployment. I'd add a CI/CD pipeline (GitHub Actions or GitLab CI) to automate the build, "
        "test, and deploy process. Helm charts would manage environment-specific configurations. The ELK stack "
        "or a managed logging service would provide observability.",
        styles['ReportBody']
    ))

    elements.append(PageBreak())
    return elements


def build_references(styles):
    """Build AI acknowledgment section"""
    elements = []

    elements.append(Paragraph("6. AI Assistance Acknowledgment", styles['SectionHeader']))

    elements.append(Paragraph("Claude (Anthropic, 2025) was used for assistance with:", styles['ReportBody']))

    ai_items = ListFlowable([
        ListItem(Paragraph("Docker Compose configuration", styles['ReportBody'])),
        ListItem(Paragraph("Kubernetes manifest templates", styles['ReportBody'])),
        ListItem(Paragraph("Helm chart structure and templates", styles['ReportBody'])),
        ListItem(Paragraph("ELK stack configuration", styles['ReportBody'])),
        ListItem(Paragraph("Preparing this report", styles['ReportBody'])),
    ], bulletType='bullet')
    elements.append(ai_items)

    return elements


def generate_report():
    """Generate the PDF report"""
    output_path = os.path.join(os.path.dirname(__file__), '..', OUTPUT_FILE)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = get_styles()
    elements = []

    # Reset figure counter
    FIGURE_COUNT[0] = 0

    # Build sections
    elements.extend(build_cover_page(styles))
    elements.extend(build_toc(styles))
    elements.extend(build_introduction(styles))
    elements.extend(build_docker_compose_section(styles))
    elements.extend(build_docker_swarm_section(styles))
    elements.extend(build_kubernetes_section(styles))
    elements.extend(build_evaluation_section(styles))
    elements.extend(build_references(styles))

    doc.build(elements, canvasmaker=NumberedCanvas)

    print(f"Report generated: {output_path}")
    print(f"Total figures: {FIGURE_COUNT[0]}")
    return output_path


if __name__ == "__main__":
    generate_report()
