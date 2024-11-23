from chat_gpt_ai import ChatGptAPI
from langchain.prompts import PromptTemplate


class RioAttractionML(ChatGptAPI):
    def __init__(self, temperature=0, model="gpt-3.5-turbo") -> None:
        super().__init__(temperature, model)

    def set_template(self):
        template = """
            Você é um assistente virtual de um aplicativo que visa montar sugestões de roteiros para turistas que estão visitando o Rio de Janeiro pela primeira vez.
            Sua função será montar uma sugestão de pontos turísticos a serem visitados em cada turno (manhã, tarde e noite) para cada dia se baseando no período em que o turista estará visitando o Rio de Janeiro, levando em consideração suas preferências pessoais, proximidades entre os pontos turísticos e o local em que o turista estará hospedado.
            Estarei lhe passando um conjunto de respostas escritas por guias turísticos para responder dúvidas de turistas.

            Siga todas as regras abaixo:
            1/ Separe a sugestão do ponto turístico separando por dia e turno. O formato deve seguir algo similar a essa estrutura: Data (Dia da Semana) - Turno - Ponto Turístico mais indicado. Exemplo: Dia 08/11/2024 (Sexta-Feira) - Manhã - Cristo Redentor
            2/ É interessante que os locais possam vim com descrição da sua localização, como o bairro em que está presente.
            3/ Cada turno em cada dia só terá um único ponto turístico de sugestão.
            4/ Cada dia sempre será considerado 3 turnos: Manhã, Tarde e Noite.
            5/ Evite repetir sugestões de pontos turísticos, o ideal é que durante toda a sugestão sempre seja colocado um local novo que ainda não foi sugerido.

            Aqui está uma possivel dúvida de um cliente nosso.
            {message}

            Aqui está uma lista de respostas escritas por guias turísticos para responder dúvidas de turistas.
            Esse histórico lhe servirá como uma guia de possíveis pontos turísticos a serem sugeridos a partir das preferências do usuário.
            {best_practice}

            Escreva uma resposta seguindo a formatação desejada para este cliente:
        """

        return template

    def set_prompt(self):
        return PromptTemplate(
            input_variables=["message", "best_practice"],
            template=self.set_template()
        )


if __name__ == "__main__":
    chat_gpt = RioAttractionML()
    chat_gpt.build_chain(path="src/openai_tourism_agent/attractions.csv", data_type="csv")
    message = "Quais pontos turisticos posso visitar, durante minha viagem, entre o dia 25/11/2024 (Segunda-feira) e 30/11/2024 (Sábado) no Rio de Janeiro? Quais pontos turisticos posso visitar, durante minha viagem, entre o dia 18/10/2024 e 20/10/2024 no Rio de Janeiro?  Estarei hospedado no bairro Copacabana e tenho preferência por conhecer os Principais Pontos Turísticos, Praias, Arquitetura e Infraestrutura Urbana."
    response = chat_gpt.generate_response(message)
    print(response)