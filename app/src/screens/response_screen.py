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
