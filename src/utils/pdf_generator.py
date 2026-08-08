"""
PDF Generator for RuralCareAI
"""

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer


class PDFGenerator:

    @staticmethod
    def generate_consultation_report(
        filename,
        patient,
        prediction,
        symptoms,
        doctor_notes,
    ):

        styles = getSampleStyleSheet()

        pdf = SimpleDocTemplate(filename)

        story = []

        story.append(
            Paragraph(
                "<b>RuralCareAI</b>",
                styles["Title"],
            )
        )

        story.append(
            Paragraph(
                "AI-Based Rural Healthcare Triage Assistant",
                styles["Heading2"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Patient Details</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                f"Patient ID : {patient.patient_code}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Name : {patient.full_name}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Age : {patient.age}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Gender : {patient.gender}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Village : {patient.village}",
                styles["Normal"],
            )
        )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "<b>Symptoms</b>",
                styles["Heading2"],
            )
        )

        for symptom in symptoms:

            story.append(
                Paragraph(
                    f"• {symptom}",
                    styles["Normal"],
                )
            )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "<b>Prediction</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                f"Disease : {prediction['predicted_disease']}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Confidence : {prediction['confidence']:.2f} %",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Risk : {prediction['risk_level']}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                prediction["recommendation"],
                styles["Normal"],
            )
        )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "<b>Doctor Notes</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                doctor_notes or "N/A",
                styles["Normal"],
            )
        )

        pdf.build(story)