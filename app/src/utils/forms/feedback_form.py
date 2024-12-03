import streamlit as st
from datetime import datetime
import re

class FeedbackForm:
    def display_form(self):
        st.header("Feedback do Roteiro de Viagem")
        st.write("Por favor, preencha o formulário abaixo para nos ajudar a melhorar nossos roteiros de viagem.")

        with st.form(key='feedback_form'):
            rating = st.slider("Avaliação do Roteiro (1-5)", min_value=1, max_value=5, step=1)

            comments = st.text_area("Comentários Adicionais", max_chars=120, help="Adicione quaisquer comentários adicionais.")

            submit_button = st.form_submit_button(label='Enviar Feedback')

        if submit_button:
            if self.validate_inputs(rating):
                st.success("Obrigado pelo seu feedback!")
                self.display_feedback_details(rating, comments)

    def validate_inputs(self, rating):
        if not (1 <= rating <= 5):
            st.error("A avaliação deve ser um número entre 1 e 5.")
            return False

        return True

    def display_feedback_details(self, rating, comments):
        st.markdown("---")
        st.write("### Detalhes do Feedback:")
        st.write(f"**Avaliação do Roteiro:** {rating}")
        st.write(f"**Comentários Adicionais:** {comments}")
