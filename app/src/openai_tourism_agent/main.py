from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader

load_dotenv()


class ChatGptAPI:
    def __init__(self, temperature=0, model="gpt-3.5-turbo") -> None:
        self.loader = CSVLoader(file_path="openai_tourism_agent/info.csv")
        documents = self.loader.load()

        embeddings = OpenAIEmbeddings()
        self.db = FAISS.from_documents(documents, embeddings)

        self.llm = ChatOpenAI(temperature=temperature, model=model)

        self.prompt = PromptTemplate(
            input_variables=["message", "best_practice_attr", "best_practice_food"],
            template=self.template()
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def retrieve_info(self, query):
        similar_response = self.db.similarity_search(query, k=3)
        return [doc.page_content for doc in similar_response]

    def set_template(self):
        template = """
            Você é um assistente virtual de um aplicativo que visa montar sugestões de roteiros para turistas que estão visitando o Rio de Janeiro pela primeira vez.
            Sua função será montar uma sugestão de pontos turísticos a serem visitados em cada turno (manhã, tarde e noite) para cada dia se baseando no período em que o turista estará visitando o Rio de Janeiro, levando em consideração suas preferências pessoais, proximidades entre os pontos turísticos e o local em que o turista estará hospedado.
            Estarei lhe passando um conjunto de dados organizados por guias turísticos para com referências de atrações. Esse conjunto de dados contém a categoria, descrição do ponto turístico, turnos e dias de funcionamento.

            Além disso, também irei encaminhar um conjunto de dados com sugestões de restaurantes, com a especialidade do restaurante e o nível de custo de alimentação de cada um.
            Em relação ao nível de custo, quanto mais $ conter, mais caro é a refeição. Assim se a pessoa preferir restaurantes que o custo de alimentação seja, no máximo, $$, você só poderá indicar restaurantes que sejam $ e $$, incluindo as categorias desejadas.

            Siga todas as regras abaixo:
            1/ Separe a sugestão do ponto turístico e restaurantes separando por dia e turno.
            2/ O formato para os pontos turísticos deve seguir algo similar a essa estrutura: Data (Dia da Semana) - Turno - Ponto Turístico mais indicado. Exemplo: Dia 08/11/2024 (Sexta-Feira) - Manhã - Cristo Redentor
            3/ O formato para os restaurantes deve seguir algo similar a essa estrutura: Data (Dia da Semana) - Turno - Restaurante mais indicado (Nível do custo de alimentação). Exemplo: Dia 08/11/2024 (Sexta-Feira) - Almoço - Bar do Bode ($)
            4/ É interessante que os locais possam vim com descrição da sua localização, como o bairro em que está presente.
            5/ Cada turno em cada dia só terá um único ponto turístico ou restaurante de sugestão.
            6/ Cada dia sempre será considerado 5 turnos: Manhã, Almoço, Tarde, Jantar e Noite.
            7/ Os pontos turísticos serão alocados apenas nos turnos Manhã, Tarde e Noite.
            8/ Os restaurantes serão alocados apenas nos turnos Almoço e Jantar.
            9/ Considere se o local estará aberto naquele turno para o dia de semana que está sendo indicado.

            Aqui está uma possivel dúvida de um cliente nosso.
            {message}

            Aqui está uma lista de pontos turísticos e suas informações.
            Esse histórico lhe servirá como uma guia de possíveis pontos turísticos a serem sugeridos a partir das preferências do usuário.
            {best_practice_attr}

            Aqui está uma lista de restaurantes e suas informações.
            Esse histórico lhe servirá como uma guia de possíveis restaurantes a serem sugeridos a partir das preferências do usuário.
            {best_practice_food}

            Escreva uma resposta seguindo a formatação desejada para este cliente:
        """

        return template

    def generate_response(self, message):
        best_practice = self.retrieve_info(message)
        response = self.chain.run(message=message, best_practice=best_practice)
        return response