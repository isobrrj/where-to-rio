import streamlit as st
from fpdf import FPDF

class PDFGenerator:
    """
    Classe responsável por gerar o PDF do roteiro de viagem.
    """

    def __init__(self, trip):
        self.trip = trip

    def generate_pdf(self):
        """
        Gera o PDF com o conteúdo do roteiro de viagem.
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt="Roteiro de Viagem", ln=True, align="C")

        for day in self.trip.days:
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(200, 10, txt=f"{day.day_of_week.upper()} - {day.date}", ln=True, align="L")

            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="Manhã:", ln=True, align="L")
            for activity in day.morning or ["Nenhuma atividade"]:
                pdf.cell(10)
                pdf.cell(0, 10, txt=f"- {activity}", ln=True, align="L")

            pdf.cell(200, 10, txt="Almoço:", ln=True, align="L")
            pdf.cell(10)
            pdf.cell(0, 10, txt=f"- {day.lunch or 'Nenhuma atividade'}", ln=True, align="L")

            pdf.cell(200, 10, txt="Tarde:", ln=True, align="L")
            for activity in day.afternoon or ["Nenhuma atividade"]:
                pdf.cell(10)
                pdf.cell(0, 10, txt=f"- {activity}", ln=True, align="L")

            pdf.cell(200, 10, txt="Noite:", ln=True, align="L")
            for activity in day.evening or ["Nenhuma atividade"]:
                pdf.cell(10)
                pdf.cell(0, 10, txt=f"- {activity}", ln=True, align="L")

            pdf.cell(200, 10, txt="Jantar:", ln=True, align="L")
            pdf.cell(10)
            pdf.cell(0, 10, txt=f"- {day.dinner or 'Nenhuma atividade'}", ln=True, align="L")

            pdf.cell(0, 10, txt="", ln=True) 

        # Salvar o PDF no caminho especificado
        pdf_path = "roteiro_viagem.pdf"
        pdf.output(pdf_path)
        return pdf_path


class ResponseScreen:
    """
    Classe responsável por renderizar a tela de resposta.
    """

    def __init__(self, trip):
        self.trip = trip
        self.pdf_generator = PDFGenerator(trip)

    def render(self):
        """
        Renderiza a página do roteiro de viagem.
        """
        st.markdown(
            """
            <h1 style="text-align: center;font-family: Montserrat; font-size: 36px; color: #333;">
                Roteiro de Viagem
            </h1>
            """,
            unsafe_allow_html=True
        )

        # Botão para exportar o PDF
        pdf_path = self.pdf_generator.generate_pdf()
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Gerar PDF",
                data=pdf_file,
                file_name="Roteiro_de_Viagem.pdf",
                mime="application/pdf",
            )

        # Estilos adicionais para o layout dos dias
        st.markdown(
            """
            <style>
            .day-container {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
                background-color: #f9f9f9;
                text-align: center;
            }
            .day-header {
                font-size: 16px;
                font-weight: bold;
                background-color: #005f73;
                color: white;
                padding: 8px;
                border-radius: 6px;
                margin-bottom: 10px;
            }
            .activity-section {
                margin: 5px 0;
                padding: 5px;
                border-radius: 6px;
            }
            .morning { background-color: #caf0f8; }
            .afternoon { background-color: #90e0ef; }
            .evening { background-color: #0077b6; color: white; }
            .meal { background-color: #03045e; color: white; }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Exibir os dias do roteiro em colunas
        columns = st.columns(len(self.trip.days))  # Criar uma coluna para cada dia

        for i, day in enumerate(self.trip.days):
            with columns[i]:
                st.markdown(
                    f"""
                    <div class="day-container">
                        <div class="day-header">{day.day_of_week.upper()}<br>{day.date}</div>
                        <div class="activity-section morning">
                            <strong>Manhã</strong><br>
                            {"<br>".join(day.morning) if day.morning else "Nenhuma atividade"}
                        </div>
                        <div class="activity-section meal">
                            <strong>Almoço</strong><br>
                            {day.lunch or "Nenhuma atividade"}
                        </div>
                        <div class="activity-section afternoon">
                            <strong>Tarde</strong><br>
                            {"<br>".join(day.afternoon) if day.afternoon else "Nenhuma atividade"}
                        </div>
                        <div class="activity-section evening">
                            <strong>Noite</strong><br>
                            {"<br>".join(day.evening) if day.evening else "Nenhuma atividade"}
                        </div>
                        <div class="activity-section meal">
                            <strong>Jantar</strong><br>
                            {day.dinner or "Nenhuma atividade"}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )