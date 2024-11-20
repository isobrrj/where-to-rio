import streamlit as st
from base_screen import render_navbar, render_footer, apply_custom_styles, render_banner
from test_trip_guide import trip

# Configuração inicial
st.set_page_config(page_title="Roteiro de Viagem", layout="wide")

# Aplicar estilos customizados
apply_custom_styles()

# Renderizar navbar e banner
render_navbar()
render_banner()

# Título da página
st.markdown(
    """
    <h1 style="text-align: center;font-family: Montserrat; font-size: 36px; color: #333;">
        Roteiro de Viagem
    </h1>
    """,
    unsafe_allow_html=True
)

# Botão para exportar (apenas visual por enquanto)
st.button("Gerar PDF")

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
columns = st.columns(len(trip.days))  # Criar uma coluna para cada dia

for i, day in enumerate(trip.days):
    with columns[i]:  # Adicionar conteúdo à coluna específica
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

render_footer()
