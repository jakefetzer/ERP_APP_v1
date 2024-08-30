from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf(order, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']

    # Title
    elements.append(Paragraph("Purchase Order", title_style))
    elements.append(Spacer(1, 12))

    # Order details
    elements.append(Paragraph(f"Order Number: {order.purchase_order_number}", subtitle_style))
    elements.append(Paragraph(f"Supplier: {order.supplier}", normal_style))
    elements.append(Paragraph(f"Status: {order.status}", normal_style))
    elements.append(Paragraph(f"Order Date: {order.order_date.strftime('%Y-%m-%d')}", normal_style))
    elements.append(Paragraph(f"Receipt Date: {order.receipt_date.strftime('%Y-%m-%d') if order.receipt_date else 'N/A'}", normal_style))
    elements.append(Spacer(1, 12))

    # Order items
    data = [['Item', 'Description', 'Quantity', 'Unit Price', 'Total']]
    
    total_price = 0
    for item in order.items:
        item_total = item.quantity * item.unit_price
        total_price += item_total
        data.append([
            item.item.item_number,
            item.item.description,
            str(item.quantity),
            f"${item.unit_price:.2f}",
            f"${item_total:.2f}"
        ])

    table = Table(data, colWidths=[1.5*inch, 2*inch, 1*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Total
    elements.append(Paragraph(f"Total: ${total_price:.2f}", subtitle_style))

    # Build the PDF
    doc.build(elements)