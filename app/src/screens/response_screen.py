from datetime import timedelta
from page_manager import PageManager
import streamlit as st
from tripguide.itinerary_manager import ItineraryManager
from tripguide.attraction_manager import AttractionManager

class ResponseScreen:
    """
    Classe responsável por renderizar a tela de resposta.
    """

    def __init__(self, user_id):
        self.user_id = user_id
        self.itinerary_manager = ItineraryManager()
        self.attraction_manager = AttractionManager()

    # def generate_pdf(self):
            
    #         """
    #         Gera o PDF com o conteúdo do roteiro de viagem.
    #         """
    #         pdf = FPDF()
    #         pdf.set_auto_page_break(auto=True, margin=15)
    #         pdf.add_page()
    #         pdf.set_font("Arial", size=12)
    #         pdf.set_font("Arial", style="B", size=16)
    #         pdf.cell(200, 10, txt="Roteiro de Viagem", ln=True, align="C")
    #         for day in self.itinerary_data:
    #             pdf.set_font("Arial", style="B", size=14)
    #             pdf.cell(200, 10, txt=f"{day['day_of_week'].upper()} - {day['date']}", ln=True, align="L")

    #             pdf.set_font("Arial", size=12)
    #             for period, activities in day['activities'].items():
    #                 pdf.cell(200, 10, txt=f"{period.capitalize()}:", ln=True, align="L")
    #                 for activity in activities or ["Nenhuma atividade"]:
    #                     pdf.cell(10)
    #                     pdf.cell(0, 10, txt=f"- {activity}", ln=True, align="L")

    #             pdf.cell(0, 10, txt="", ln=True)
    #         # Salvar o PDF no caminho especificado
    #         pdf_path = "roteiro_viagem.pdf"
    #         pdf.output(pdf_path)
    #         return pdf_path

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

        itinerary_args = PageManager.get_page_args()
        itinerary_id = itinerary_args.get("itinerary_id")

        if not itinerary_id:
            st.warning("Roteiro não encontrado.")
            return

        itinerary_data = self.itinerary_manager.get_itinerary_data(itinerary_id=itinerary_id)
        if not itinerary_data:
            st.warning("Nenhum roteiro encontrado para o usuário.")
            return
        
        # # Botão para exportar o PDF
        # pdf_generator = PDFGenerator(itinerary_data)
        # pdf_path = pdf_generator.generate_pdf()
        # with open(pdf_path, "rb") as pdf_file:
        #     st.download_button(
        #         label="Gerar PDF",
        #         data=pdf_file,
        #         file_name="Roteiro_de_Viagem.pdf",
        #         mime="application/pdf",
        #     )
        
        # Dicionário para traduzir os dias da semana
        days_translation = {
            "Monday": "Segunda-feira",
            "Tuesday": "Terça-feira",
            "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira",
            "Friday": "Sexta-feira",
            "Saturday": "Sábado",
            "Sunday": "Domingo",
        }

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
            </style>
            """,
            unsafe_allow_html=True
        )

        # Dados do itinerário
        activities = itinerary_data.get("activities", {})
        dates = [
            {"date": itinerary_data["start_date"], "day_of_week": "Segunda-feira"},
            {"date": itinerary_data["end_date"], "day_of_week": "Quarta-feira"},
        ]  # Ajuste a lógica para preencher dias corretamente

        dates = []
        current_date = itinerary_data["start_date"]
        end_date = itinerary_data["end_date"]

        while current_date <= end_date:
            dates.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "day_of_week": current_date.strftime("%A")
            })
            current_date += timedelta(days=1)

        # Criar colunas para cada dia
        days = itinerary_data.get("days", [])
        columns = st.columns(len(days))  # Criar uma coluna para cada dia

        for col, day_info in zip(columns, days):
            date = day_info.get("date", "Data Desconhecida").strftime("%d/%m/%Y")
            day_of_week_en = day_info.get("day_of_week", "Dia Desconhecido")
            day_of_week_pt = days_translation.get(day_of_week_en, day_of_week_en)
            activities = day_info.get("activities", {"morning": [], "afternoon": [], "evening": []})

            with col:

                st.markdown(
                    f"""
                    <div class="day-container">
                        <div class="day-header">
                            {date}<br>{day_of_week_pt}
                        </div>
                        <div class="activity-section morning">
                            <strong>Manhã</strong><br>
                            {"<br>".join(activity.get('name', 'Atividade sem Nome') for activity in activities.get('morning', [])) or "Nenhuma atividade"}
                        </div>
                        <div class="activity-section afternoon">
                            <strong>Tarde</strong><br>
                            {"<br>".join(activity.get('name', 'Atividade sem Nome') for activity in activities.get('afternoon', [])) or "Nenhuma atividade"}
                        </div>
                        <div class="activity-section evening">
                            <strong>Noite</strong><br>
                            {"<br>".join(activity.get('name', 'Atividade sem Nome') for activity in activities.get('evening', [])) or "Nenhuma atividade"}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
