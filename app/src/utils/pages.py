import streamlit as st
from utils.forms.feedback_form import FeedbackForm
from utils.index.home import Home

class Pages:
    def page_flow(self):
        home = Home()
        feedback_form = FeedbackForm()

        routes = {
            "Home": home.home_page,
            "feedback": feedback_form.display_form
        }

        st.sidebar.title("Menu")
        page_choice = st.sidebar.selectbox("Navegar para", list(routes.keys()))
        routes[page_choice]()
    