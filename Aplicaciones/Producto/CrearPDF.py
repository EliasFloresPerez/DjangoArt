from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.units import cm
from decimal import Decimal
from PIL import Image as PILImage
from io import BytesIO
import os

def generar_pdf_retiro_raee_bytes(datos, titulo, filtro):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elementos = []

    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_title.alignment = 1  # Centrado

    # Imagen de cabecera
    cabecera_path = "Aplicaciones/Producto/cabecera.png"
    if os.path.exists(cabecera_path):
        img = PILImage.open(cabecera_path)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        header_img = Image(cabecera_path, width=16*cm, height=(16*aspect)*cm)
        elementos.append(header_img)
        elementos.append(Spacer(1, 0.5*cm))

    # Título
    elementos.append(Paragraph(titulo, style_title))
    elementos.append(Spacer(1, 0.5*cm))

    # Cabecera de tabla
    data = [["ITEM", filtro, "KGS"]]
    total = 0

    for i, d in enumerate(datos, start=1):
        empresa = d["Datos"]
        peso = float(d["total_peso"])
        data.append([i, empresa, f"{peso:.2f}"])
        total += peso

    data.append(["", "TOTAL GENERAL", f"{total:.2f}"])

    # Tabla
    tabla = Table(data, colWidths=[2*cm, 10*cm, 3*cm])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 1*cm))

    # Imagen de pie
    footer_path = "Aplicaciones/Producto/Fotter.png"
    if os.path.exists(footer_path):
        img = PILImage.open(footer_path)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        footer_img = Image(footer_path, width=16*cm, height=(16*aspect)*cm)
        elementos.append(footer_img)

    # Crear PDF en memoria
    doc.build(elementos)

    # Preparar BytesIO para lectura externa
    buffer.seek(0)
    return buffer
