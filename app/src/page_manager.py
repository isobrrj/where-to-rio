import streamlit as st
import logging

class PageManager:
    """
    Classe responsável por gerenciar a navegação entre páginas.
    """

    current_page = None
    page_args = {}

    def __init__(self, cookie_manager):
        """
        Inicializa o gerenciador de páginas.
        :param cookie_manager: Gerenciador de cookies para manter o estado.
        """
        self.cookie_manager = cookie_manager
        self.default_page = "Home"

        # Configurações de logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # Mapeamento de páginas (diferenciando se precisam de cookie_manager ou não)
        self.page_map = {
            "Home": ("screens.home_screen.HomeScreen", False),
            "Login": ("screens.login_screen.LoginScreen", True),
            "Register": ("screens.register_screen.RegisterScreen", False),
            "Meus Roteiros": ("screens.itinerarylist_screen.ItineraryListScreen", True),
            "Roteiro": ("screens.response_screen.ResponseScreen", True),
            "RequestScreen": ("screens.request_screen.RequestScreen", False),
        }

    @staticmethod
    def set_page(page_name, **kwargs):
        """
        Define a página atual e armazena argumentos opcionais.
        :param page_name: Nome da página.
        :param kwargs: Argumentos opcionais para passar dados entre páginas.
        """
        PageManager.current_page = page_name
        PageManager.page_args = kwargs
        st.session_state["current_page"] = page_name
        st.rerun()

    def get_page(self):
        """
        Retorna a página atual definida no estado global.
        """
        return st.session_state.get("current_page", self.default_page)
    
    @staticmethod
    def get_page_args():
        """
        Recupera os argumentos passados para a página atual.
        :return: Dicionário com os argumentos da página.
        """
        return PageManager.page_args

    def render_current_page(self):
        """
        Gerencia e renderiza a página atual com base no estado de navegação.
        """
        current_page = self.get_page()

        # Verificar permissões antes de renderizar a página
        if current_page == "Meus Roteiros" and not st.session_state.get("logged_in", False):
            st.warning("Por favor, faça login para acessar Meus Roteiros.")
            self.set_page("Login")
            return None

        if current_page == "Register" and st.session_state.get("logged_in", False):
            st.warning("Você já está registrado e logado.")
            self.set_page("Home")
            return None

        # Renderizar a página correspondente
        if current_page in self.page_map:
            page_class_path, needs_cookie_manager = self.page_map[current_page]
            return self._render_page(page_class_path, needs_cookie_manager)
        else:
            st.error(f"Página não encontrada: {current_page}")
            return None

    def _render_page(self, page_class_path, needs_cookie_manager):
        """
        Importa e renderiza dinamicamente a página usando seu caminho.
        :param page_class_path: Caminho completo da classe da página (ex: 'screens.home_screen.HomeScreen')
        :param needs_cookie_manager: Se a página requer o cookie manager
        """
        try:
            # Dividir o caminho do módulo e a classe
            module_path, class_name = page_class_path.rsplit(".", 1)

            # Importar o módulo e acessar a classe
            module = __import__(module_path, fromlist=[class_name])
            page_class = getattr(module, class_name)

            # Inicializar a classe com ou sem o cookie manager
            if needs_cookie_manager:
                page_instance = page_class(self.cookie_manager)
            else:
                page_instance = page_class()

            # Verificar e chamar o método render
            if hasattr(page_instance, "render"):
                return page_instance.render()
            else:
                st.error(f"A classe {class_name} não possui o método render.")
                return None
        except (ImportError, AttributeError, ValueError) as e:
            st.error(f"Erro ao carregar a página {page_class_path}: {e}")
            return None

