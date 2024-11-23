from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader

load_dotenv()


class ChatGptAPI:
    def __init__(self, temperature=0, model="gpt-3.5-turbo", csv_path="") -> None:
        if len(csv_path) > 0:
            documents = self.load_documents_from_csv(csv_path)

        embeddings = OpenAIEmbeddings()
        self.db = FAISS.from_documents(documents, embeddings)

        self.llm = ChatOpenAI(temperature=temperature, model=model)

        self.prompt = PromptTemplate(
            input_variables=["message", "best_practice"],
            template=self.set_template()
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def load_documents_from_csv(self, path):
        self.loader = CSVLoader(file_path=path)
        documents = self.loader.load()
        return documents

    def retrieve_info(self, query):
        similar_response = self.db.similarity_search(query, k=3)
        return [doc.page_content for doc in similar_response]

    def set_template(self):
        template = """
            Você é um assistente virtual de um aplicativo que visa montar sugestões de roteiros para turistas que estão visitando o Rio de Janeiro pela primeira vez.
            Sua função será montar uma sugestão de pontos turísticos a serem visitados em cada turno (manhã, tarde e noite) para cada dia se baseando no período em que o turista estará visitando o Rio de Janeiro, levando em consideração suas preferências pessoais, proximidades entre os pontos turísticos e o local em que o turista estará hospedado.
            Estarei lhe passando um conjunto de dados organizados por guias turísticos para com referências de pontos turísticos. Esse conjunto de dados contém a categoria, descrição do local, dias e turnos de funcionamento, e localização.

            Siga todas as regras abaixo:
            1/ Separe a sugestão do ponto turístico separando por dia e turno.
            2/ O formato para os pontos turísticos deve seguir algo similar a essa estrutura: Data (Dia da Semana) - Turno - Ponto Turístico mais indicado. Exemplo: Dia 08/11/2024 (Sexta-Feira) - Manhã - Cristo Redentor
            3/ É interessante que os locais possam vim com descrição da sua localização, como o bairro em que está presente.
            5/ Cada turno em cada dia só terá um único ponto turístico de sugestão.
            6/ Cada dia sempre será considerado 3 turnos: Manhã, Tarde e Noite.
            7/ Considere se o local estará funcionando naquele turno para o dia de semana e turno que está sendo indicado.

            Aqui está uma possivel dúvida de um cliente nosso.
            {message}

            Aqui está uma lista de pontos turísticos, com suas informações respectivas.
            Esse histórico lhe servirá como uma guia de possíveis pontos turísticos a serem sugeridos a partir das preferências do usuário.
            {best_practice}

            Escreva uma resposta seguindo a formatação desejada para este cliente:
        """

        return template

    def generate_response(self, message):
        best_practice = self.retrieve_info(message)
        response = self.chain.run(message=message, best_practice=best_practice)
        return response

if __name__ == "__main__":
    chat_gpt = ChatGptAPI(csv_path="src/openai_tourism_agent/attractions.csv")
    message = "Irei conhecer o Rio de Janeiro entre o dia 2024-11-26 e 2024-11-30. Estarei hospedado no bairro Copacabana e tenho preferência por conhecer atrações nas seguintes categorias: Parques e Trilhas, Principais Pontos Turísticos, Entretenimento e Lazer, Arquitetura e Urbanismo, Patrimônio Histórico e Cultural. Que pontos turístico poderia conhecer durante minha estadia?"
    response = chat_gpt.generate_response(message)
    print(response)