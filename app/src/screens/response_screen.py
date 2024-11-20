import streamlit as st
from base_screen import render_navbar, render_footer, render_background, apply_custom_styles
from tripguide.test_trip_guide import trip

# Configuração inicial
st.set_page_config(page_title="Roteiro de Viagem", layout="wide")

# Aplicar estilos customizados
apply_custom_styles()

# Renderizar navbar e background
render_navbar()
render_background()

# Conteúdo principal (exemplo do roteiro)
st.title("Roteiro Gerado")

if trip.days:
    for day in trip.days:
        st.subheader(f"{day.date} ({day.day_of_week})")
        st.write(f"**Café da Manhã:** {day.breakfast or 'Nenhuma atividade'}")

        st.write("**Manhã:**")
        if day.morning:
            for activity in day.morning:
                st.write(f"- {activity}")
        else:
            st.write("Nenhuma atividade")

        st.write(f"**Almoço:** {day.lunch or 'Nenhuma atividade'}")

        st.write("**Tarde:**")
        if day.afternoon:
            for activity in day.afternoon:
                st.write(f"- {activity}")
        else:
            st.write("Nenhuma atividade")

        st.write("**Noite:**")
        if day.evening:
            for activity in day.evening:
                st.write(f"- {activity}")
        else:
            st.write("Nenhuma atividade")

        st.write(f"**Jantar:** {day.dinner or 'Nenhuma atividade'}")

        st.markdown("---")
else:
    st.write("Nenhum dia foi adicionado ao roteiro.")

# Renderizar footer
render_footer()
