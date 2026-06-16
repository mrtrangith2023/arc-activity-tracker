from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

def generate_pdf(data):

    filename = "wallet_report.pdf"

    doc = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Arc Wallet Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"Address: {data['address']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Balance: {data['balance']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Score: {data['score']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Badge: {data['badge']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Risk: {data['risk']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Grade: {data['grade']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Protocols: {data['protocol_count']}",
            styles["Normal"]
        )
    )

    doc.build(content)

    return filename