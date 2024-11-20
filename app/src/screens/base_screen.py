import streamlit as st

def render_navbar():
    st.markdown(
        """
        <div class="navbar">
            <div class="navbar-logo">
                <img src="https://upload.wikimedia.org/wikipedia/commons/9/9a/Google_Maps_icon.svg" alt="Logo">
                <span>WHEREtorio</span>
            </div>
            <div class="navbar-links">
                <a href="#">Home</a>
                <a href="#">Meus Roteiros</a>
                <a href="#">Sobre</a>
            </div>
            <div class="user-info">
                <span>Olá, Usuário!</span>
                <button>Sair</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_footer():
    st.markdown(
        """
        <div class="footer">
            © 2024 WHEREtorio - Todos os direitos reservados
        </div>
        """,
        unsafe_allow_html=True
    )


def render_background():
    st.markdown(
        """
        <div class="background-image">
            <div class="title">WHEREtorio</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# CSS customizado
def apply_custom_styles():
    st.markdown(
        """
        <style>
        .navbar {
            background-color: #023e8a;
            padding: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            font-family: Arial, sans-serif;
            font-size: 18px;
        }
        .navbar-logo {
            display: flex;
            align-items: center;
        }
        .navbar-logo img {
            height: 40px;
            margin-right: 10px;
        }
        .navbar-links {
            display: flex;
            gap: 20px;
        }
        .navbar-links a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
        .navbar-links a:hover {
            text-decoration: underline;
        }
        .user-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .user-info button {
            background-color: #90e0ef;
            border: none;
            color: #023e8a;
            padding: 5px 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        .user-info button:hover {
            background-color: #0077b6;
            color: white;
        }
        .footer {
            background-color: #023e8a;
            color: white;
            text-align: center;
            padding: 10px 0;
            position: fixed;
            bottom: 0;
            width: 100%;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        .background-image {
            width: 100%;
            height: 200px;
            background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Rio_de_Janeiro_%2811%29.jpg/1920px-Rio_de_Janeiro_%2811%29.jpg');
            background-size: cover;
            background-position: center;
            position: relative;
        }
        .background-image .title {
            position: absolute;
            bottom: 20px;
            left: 20px;
            color: white;
            font-size: 36px;
            font-weight: bold;
            text-shadow: 1px 1px 4px black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
