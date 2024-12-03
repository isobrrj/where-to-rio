from openai_tourism_agent.chat_gpt_ai import ChatGptAPI
from langchain.prompts import PromptTemplate


class RioAttractionML(ChatGptAPI):
    def __init__(self, temperature=0, model="gpt-3.5-turbo") -> None:
        super().__init__(temperature, model)

    def set_template(self):
        template = """
            Você é um assistente virtual de um aplicativo que visa montar sugestões de roteiros para turistas que estão visitando o Rio de Janeiro pela primeira vez.
            Sua função será montar uma sugestão de atrações a serem visitadas em cada turno (manhã, tarde e noite) para cada dia se baseando no período em que o turista estará visitando o Rio de Janeiro, levando em consideração suas preferências pessoais.
            Estarei lhe passando um conjunto de atrações agrupadas por categoria de atração que servirá como um guia auxiliar de acordo com a preferência do usuário, além de conter a descrição e localização que deve ser anexada a sua resposta.
            
            Siga todas as regras abaixo, estritamente:
            1/ Separe a sugestão da atração separando por dia e turno. O formato deve seguir exatamente essa estrutura: Data (Dia da Semana) - Turno - Atração. Exemplo de uso: Dia 08/11/2024 (Sexta-Feira) - Manhã - Cristo Redentor
            2/ As atrações devem vim com a descrição e localização.
            3/ Cada turno em cada dia só terá uma única atração de sugestão.
            4/ Cada dia sempre terá sempre 3 turnos: Manhã, Tarde e Noite.
            5/ Evite repetir sugestões de atrações entre diferentes dias e turnos, o ideal é que durante toda a sugestão sempre seja colocado uma nova atração que ainda não foi sugerido.
            6/ Todos os dias e turnos devem ser preenchidos com alguma sugestão.
            Aqui está a dúvida do nosso cliente.
            {message}

            Aqui está uma lista de atrações categorizadas com informações de descrição e localização.
            Esse conjunto de dados lhe servirá como uma guia de possíveis atrações a serem sugeridos a partir das preferências do usuário.
            {best_practice}

            Fique a vontade de buscar de fonte externas outras atrações similares, seguindo as regras estabelecidas.

            Escreva uma resposta seguindo as regras estabelecidas para este cliente:
        """

        return template

    def set_prompt(self):
        return PromptTemplate(
            input_variables=["message", "best_practice"],
            template=self.set_template()
        )


if __name__ == "__main__":
    chat_gpt = RioAttractionML()
    chat_gpt.load_documents_from_csv(path="src/openai_tourism_agent/attractions.csv")
    chat_gpt.build_chain()
    message = "Quais pontos turisticos posso visitar, durante minha viagem, entre o dia 25/11/2024 (Segunda-feira) e 30/11/2024 (Sábado) no Rio de Janeiro? Quais pontos turisticos posso visitar, durante minha viagem, entre o dia 18/10/2024 e 20/10/2024 no Rio de Janeiro?  Estarei hospedado no bairro Copacabana e tenho preferência por conhecer os Principais Pontos Turísticos, Praias, Arquitetura e Infraestrutura Urbana."
    response = chat_gpt.generate_response(message)
    print(response)
