from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader
from abc import ABC, abstractmethod

load_dotenv()


class ChatGptAPI(ABC):
    def __init__(self, temperature=0, model="gpt-3.5-turbo") -> None:
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=temperature, model=model)

    def load_documents_from_csv(self, path):
        loader = CSVLoader(file_path=path)
        return loader.load()

    def load_document(self, path, data_type):
        if data_type == "csv":
            documents = self.load_documents_from_csv(path)
            return documents

    def build_chain(self, path, data_type):
        self.documents = self.load_document(path, data_type)
        self.prompt = self.set_prompt()
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def retrieve_info(self, query):
        if not self.documents:
            raise Exception("É necessário realizar o carregamento dos documentos! Utilize o método build_chain para carregar documentos e definir prompt.")
        db = FAISS.from_documents(self.documents, self.embeddings)
        similar_response = db.similarity_search(query, k=3)
        return [doc.page_content for doc in similar_response]

    def generate_response(self, message):
        best_practice = self.retrieve_info(message)
        response = self.chain.run(message=message, best_practice=best_practice)
        return response

    @abstractmethod
    def set_template(self):
        pass

    @abstractmethod
    def set_prompt(self):
        pass