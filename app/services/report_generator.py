from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from typing import Dict, Any
from datetime import datetime
import io

class ReportGenerator:
    """Generate PDF reports for assessments"""
    
    @staticmethod
    def generate_pdf(assessment_data: Dict[str, Any], output_path: str = None) -> bytes:
        """
        Generate a PDF report from assessment data
        Returns bytes if output_path is None, otherwise saves to file
        """
        buffer = io.BytesIO() if output_path is None else None
        doc = SimpleDocTemplate(
            buffer if buffer else output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            leading=14,
            alignment=TA_JUSTIFY
        )
        
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#E74C3C'),
            leading=12,
            alignment=TA_CENTER,
            backColor=colors.HexColor('#FADBD8'),
            borderPadding=10
        )
        
        # Title
        elements.append(Paragraph("OvaSense AI Assessment Report", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Date
        date_str = datetime.now().strftime("%B %d, %Y")
        elements.append(Paragraph(f"<i>Generated on: {date_str}</i>", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # IMPORTANT DISCLAIMER
        disclaimer_text = (
            "<b>IMPORTANT DISCLAIMER:</b><br/>"
            "This is not a medical diagnosis. This report provides risk assessment and pattern "
            "detection based on self-reported information. Please consult a qualified healthcare "
            "professional for proper medical evaluation and diagnosis."
        )
        elements.append(Paragraph(disclaimer_text, disclaimer_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        elements.append(Paragraph("Executive Summary", heading_style))
        
        risk_level = assessment_data.get('risk_level', 'Unknown')
        phenotype = assessment_data.get('phenotype', 'Unknown')
        confidence = assessment_data.get('confidence_score', 0) * 100
        risk_score = assessment_data.get('risk_score', 0)
        
        summary_text = (
            f"Your assessment indicates a <b>{risk_level}</b> risk level "
            f"(Risk Score: {risk_score:.1f}%) with a <b>{phenotype}</b> pattern. "
            f"The confidence level of this assessment is {confidence:.1f}%."
        )
        elements.append(Paragraph(summary_text, body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Risk Assessment Details
        elements.append(Paragraph("Risk Assessment Details", heading_style))
        
        risk_data = [
            ['Risk Level', risk_level],
            ['Risk Score', f"{risk_score:.1f}%"],
            ['Phenotype Pattern', phenotype],
            ['Confidence Score', f"{confidence:.1f}%"]
        ]
        
        risk_table = Table(risk_data, colWidths=[2*inch, 4*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(risk_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Key Contributing Factors
        elements.append(Paragraph("Key Contributing Factors", heading_style))
        key_drivers = assessment_data.get('key_drivers', [])
        if key_drivers:
            for driver in key_drivers:
                elements.append(Paragraph(f"• {driver}", body_style))
        else:
            elements.append(Paragraph("No specific factors identified.", body_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Phenotype Explanation
        elements.append(Paragraph("Pattern Explanation", heading_style))
        explanation = assessment_data.get('explanation', '')
        if explanation:
            elements.append(Paragraph(explanation, body_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Lifestyle Recommendations
        elements.append(Paragraph("Lifestyle Recommendations", heading_style))
        remedies = assessment_data.get('remedies', {})
        
        if isinstance(remedies, dict):
            if 'diet' in remedies:
                elements.append(Paragraph("<b>Dietary Recommendations:</b>", body_style))
                for remedy in remedies.get('diet', [])[:5]:
                    elements.append(Paragraph(f"• {remedy}", body_style))
                elements.append(Spacer(1, 0.15*inch))
            
            if 'exercise' in remedies:
                elements.append(Paragraph("<b>Exercise Recommendations:</b>", body_style))
                for remedy in remedies.get('exercise', [])[:4]:
                    elements.append(Paragraph(f"• {remedy}", body_style))
                elements.append(Spacer(1, 0.15*inch))
            
            if 'lifestyle' in remedies:
                elements.append(Paragraph("<b>Lifestyle Modifications:</b>", body_style))
                for remedy in remedies.get('lifestyle', [])[:4]:
                    elements.append(Paragraph(f"• {remedy}", body_style))
        elif isinstance(remedies, list):
            for remedy in remedies[:8]:
                elements.append(Paragraph(f"• {remedy}", body_style))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Clinical Next Steps
        elements.append(Paragraph("Suggested Clinical Next Steps", heading_style))
        next_steps = assessment_data.get('next_steps', [])
        for step in next_steps:
            elements.append(Paragraph(f"• {step}", body_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Final Disclaimer
        elements.append(PageBreak())
        elements.append(Paragraph("Important Information", heading_style))
        final_disclaimer = (
            "This assessment tool is designed to help identify patterns and risk factors "
            "associated with hormonal health. It is not a substitute for professional medical "
            "advice, diagnosis, or treatment. Always seek the advice of your physician or other "
            "qualified health provider with any questions you may have regarding a medical condition. "
            "Never disregard professional medical advice or delay in seeking it because of something "
            "you have read in this report."
        )
        elements.append(Paragraph(final_disclaimer, body_style))
        
        # Build PDF
        doc.build(elements)
        
        if buffer:
            return buffer.getvalue()
        return None

