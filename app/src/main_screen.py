import streamlit as st
from trip_guide_builder import TripGuideBuilder
from page_manager import PageManager
from screens.base_screen import BaseScreen
from streamlit_cookies_manager import EncryptedCookieManager

# Configuração inicial da página
st.set_page_config(page_title="WHEREtoRio", layout="wide")

# Inicializar o gerenciador de cookies
cookie_manager = EncryptedCookieManager(prefix="wheretoriorio", password="chave_secreta")

if not cookie_manager.ready():
    st.stop()  # Aguarda a inicialização do gerenciador de cookies

# Restaurar o estado de login a partir dos cookies
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = cookie_manager.get("logged_in", "false") == "true"
    st.session_state["user_id"] = int(cookie_manager.get("user_id", "0")) if cookie_manager.get("user_id") else None
    st.session_state["user_name"] = cookie_manager.get("user_name", "Visitante")

# Renderiza elementos comuns
navbar = BaseScreen.render_navbar(cookie_manager)
styles = BaseScreen.apply_custom_styles()
banner = BaseScreen.render_banner()

page_manager = PageManager(cookie_manager)  # Inicializa o gerenciador de páginas

# Renderiza a página atual e captura o resultado, se houver
result = page_manager.render_current_page()

# Processa o resultado, se for gerado pela página RequestScreen
if result:
    trip_guide_builder = TripGuideBuilder(tourism_preference=result)
    question = trip_guide_builder.build_question_message_llm()
    # st.write(question)
    # suggestion = trip_guide_builder.ask_chat_gpt_about_attractions(question)
    suggestion = """
        Dia 03/12/2024 (Terça-Feira) - Manhã - Maracanã Descrição: Estádio Jornalista Mário Filho, mais conhecido como Maracanã, ou carinhosamente como Maraca, é um estádio de futebol localizado no bairro de mesmo nome, na Zona Norte da cidade brasileira do Rio de Janeiro. Localização: R. Prof. Eurico Rabelo - Maracanã, Rio de Janeiro - RJ, 20271-150 Categoria de Atração: Principais Pontos Turísticos

        Dia 03/12/2024 (Terça-Feira) - Tarde - Praia de Copacabana Descrição: A Praia de Copacabana é uma praia localizada no bairro de Copacabana, na Zona Sul da cidade do Rio de Janeiro, no Brasil. É considerada uma das praias mais famosas do mundo. Localização: Copacabana; Brasil Categoria de Atração: Praias

        Dia 03/12/2024 (Terça-Feira) - Noite - Praia de Ipanema Descrição: Esta é uma praia bastante badalada no Rio, frequentada por artistas, jovens, turistas e moradores que aproveitam seu calçadão para a prática de exercícios. A praia do bairro nobre é um dos points da cidade quando o assunto é curtir o mar e tem uma parte destinada ao público LGBT+. As condições do mar dependem do período, mas muitas vezes o mar é tranquilo, com ondas fracas. Localização: Avenida Vieira Souto, Rio de Janeiro, Estado do Rio de Janeiro 22420-002 Brasil Categoria de Atração: Praias

        Dia 04/12/2024 (Quarta-Feira) - Manhã - Parque Lage Descrição: O Parque Lage é um parque público no bairro Jardim Botânico, na Zona Sul do Rio de Janeiro. Possui trilhas, jardins, um belo palacete e uma vista incrível para o Cristo Redentor. Localização: R. Jardim Botânico, 414 - Jardim Botânico, Rio de Janeiro - RJ, 22461-000 Categoria de Atração: Parques e Trilhas

        Dia 04/12/2024 (Quarta-Feira) - Tarde - Museu Histórico Nacional Descrição: O Museu Histórico Nacional é um museu localizado na Praça Marechal Âncora, no centro histórico do Rio de Janeiro. Possui um acervo que conta a história do Brasil desde a época do descobrimento. Localização: Praça Marechal Âncora, S/N - Centro, Rio de Janeiro - RJ, 20021-200 Categoria de Atração: Patrimônio Histórico e Cultural

        Dia 04/12/2024 (Quarta-Feira) - Noite - Pão de Açúcar Descrição: O Pão de Açúcar é um dos principais pontos turísticos do Rio de Janeiro. É um complexo de morros localizado na entrada da Baía de Guanabara, no bairro da Urca, com uma vista panorâmica incrível da cidade. Localização: Av. Pasteur, 520 - Urca, Rio de Janeiro - RJ, 22290-255 Categoria de Atração: Principais Pontos Turísticos

        Dia 05/12/2024 (Quinta-Feira) - Manhã - Jardim Botânico Descrição: O Jardim Botânico do Rio de Janeiro é um dos mais importantes do Brasil, com uma grande diversidade de plantas e árvores. Possui uma estufa de plantas raras, lagos e trilhas para caminhada. Localização: R. Jardim Botânico, 1008 - Jardim Botânico, Rio de Janeiro - RJ, 22460-030 Categoria de Atração: Parques e Trilhas

        Dia 05/12/2024 (Quinta-Feira) - Tarde - Museu do Amanhã Descrição: O Museu do Amanhã é um museu de ciências localizado na Praça Mauá, na região portuária do Rio de Janeiro. Possui exposições interativas sobre sustentabilidade, meio ambiente e o futuro da humanidade. Localização: Praça Mauá, 1 - Centro, Rio de Janeiro - RJ, 20081-240 Categoria de Atração: Patrimônio Histórico e Cultural

        Dia 05/12/2024 (Quinta-Feira) - Noite - Lapa Descrição: A Lapa é um bairro boêmio do Rio de Janeiro, conhecido pelos seus arcos, bares, casas de show e vida noturna agitada. É um local tradicional para quem busca diversão e música ao vivo. Localização: Lapa, Rio de Janeiro - RJ Categoria de Atração: Principais Pontos Turísticos

        Espero que aproveite sua viagem e as sugestões de roteiro!
    """
    # st.write(suggestion)
    trip_guide_day = trip_guide_builder.build_trip_guide_day(suggestion)
    st.write(str(trip_guide_day))


footer = BaseScreen.render_footer()
