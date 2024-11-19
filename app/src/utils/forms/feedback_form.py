# feedback_form.py

import streamlit as st
from datetime import datetime

class FeedbackForm:
    def display_form(self):
        st.header("Feedback do Roteiro de Viagem")
        st.write("Por favor, preencha o formulário abaixo para nos ajudar a melhorar nossos roteiros de viagem.")

        with st.form(key='feedback_form'):
            travel_date = st.date_input("Data da Viagem", min_value=datetime.today())

            rating = st.slider("Avaliação do Roteiro (1-5)", min_value=1, max_value=5, step=1)

            comments = st.text_area("Comentários Adicionais", max_chars=200, help="Adicione quaisquer comentários adicionais.")

            # Botão de Envio
            submit_button = st.form_submit_button(label='Enviar Feedback')

        if submit_button:
            if self.validate_inputs(travel_date, rating):
                st.success("Obrigado pelo seu feedback!")
                self.display_feedback_details(travel_date, rating, comments)

    def validate_inputs(self, travel_date, rating):
        if not re.match(r'\d{2}/\d{2}/\d{4}', travel_date):
            st.error("Por favor, insira a data no formato DD/MM/AAAA.")
            return False

        if travel_date < datetime.today().date():
            st.error("A data da viagem não pode estar no passado.")
            return False

        # Validação da Avaliação
        if not (1 <= rating <= 5):
            st.error("A avaliação deve ser um número entre 1 e 5.")
            return False

        return True

    def display_feedback_details(self, name, destination, travel_date, rating, comments):
        st.markdown("---")
        st.write("### Detalhes do Feedback:")
        st.write(f"**Data da Viagem:** {travel_date.strftime('%d/%m/%Y')}")
        st.write(f"**Avaliação do Roteiro:** {rating}")
        st.write(f"**Comentários Adicionais:** {comments}")
