from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
#from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

load_dotenv(find_dotenv())

#llm = ChatOllama(model="phi3", temperature=0)
#llm_cadastro = ChatOllama(model="phi3", temperature=0)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_cadastro = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Definindo os schemas de resposta
response_schemas = [
    ResponseSchema(name="nome_completo", description="Nome completo do cliente"),
    ResponseSchema(name="cpf", description="CPF do cliente"),
    ResponseSchema(name="email", description="Email do cliente"),
    ResponseSchema(name="endereco", description="Endereço do cliente"),
    ResponseSchema(name="cidade", description="Cidade do cliente"),
    ResponseSchema(name="estado", description="Estado do cliente"),
]
parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = parser.get_format_instructions()

# RouterChain
chain = (
    ChatPromptTemplate.from_template(
        """
        Classifique a pergunta do usuário em uma das seguintes categorias:
        - Cadastro de usuário
        - Configuração de ações
        - Finalizar atendimento
        - Outros

        Pergunta: {query}
        Classificação:
        """
    )
    | llm
    | StrOutputParser() 
)

# elos específicos
iniciar_cadastro_chain = ChatPromptTemplate.from_template(
    """
    Você é o assistente do aplicativo Zafira.
    O usuário está iniciando o cadastro de um novo usuário.
    Peça apenas pelos dados necessários para o cadastro.
    nome_completo: Nome completo do usuário
    cpf: CPF do usuário
    email: Email do usuário
    endereco: Endereço do usuário
    cidade: Cidade do usuário
    estado: Estado do usuário
    Pergunta: {query}
    Resposta:
    """
) | llm

construtor_JSON_cadastro_chain = (
    ChatPromptTemplate.from_messages([
        ("system", """
        Você é um assistente virtual para o aplicativo de cadastro de usuários da empresa Zafira. 
        Interprete as perguntas do usuário e avalie o texto e extraia os dados do usuário. 
        nome_completo: Nome completo do usuário
        cpf: CPF do usuário
        email: Email do usuário
        endereco: Endereço do usuário
        cidade: Cidade do usuário
        estado: Estado do usuário
        Ignore caracteres especiais.
        Caso o usuário não tenha fornecido algum desses dados, retorne None na área correspondente.
        Just return the JSON, do not add ANYTHING, NO INTERPRETATION!
        Do not return duplicate keys.
    

        {format_instructions}
        """),
        ("human", "{query}")
    ])
    | llm_cadastro
    | parser 
)

verificar_JSON_chain = (
    ChatPromptTemplate.from_messages([
        ("system", """
        Você é um verificador de dados JSON.
        Analise o JSON fornecido e verifique se todos os campos estão preenchidos corretamente.
        Retorne apenas "completo" se todos os campos estiverem preenchidos (sem None ou none).
        Retorne "incompleto" se algum campo estiver None, none ou vazio.
        Just return the word, no other text!
        """),
        ("human", "{json_data}")
    ])
    | llm_cadastro
    | StrOutputParser()
)

configuracao_chain = ChatPromptTemplate.from_template(
    """
    Você é o assistente do aplicativo Zafira.
    Essa é a função de configuração de ações do aplicativo. 
    Responda que esta área está em desenvolvimento e estará disponível em breve.
    Pergunta: {query}\n
    Resposta:
    """
) | llm

finalizar_chain = ChatPromptTemplate.from_template(
    """
    Você é o assistente do aplicativo Zafira.
    O usuário está desligando a conversa, seja educado e despeça-se do cliente.
    Pergunta: {query}
    Resposta:
    """
) | llm
nao_se_aplica_chain = ChatPromptTemplate.from_template(
    """
    Você é o assistente do aplicativo Zafira.
    Não foi possível classificar a pergunta do usuário dentro das funções disponíveis.
    Guie o cliente para escolher entre Cadastro de Clientes ou Configuração do Aplicativo.
    Pergunta: {query}
    Resposta:
    """
) | llm

def route(info):
    topic = info["topic"].lower()
    query = info["query"]
    
    if "cadastro" in topic:
        return realizar_cadastro(query, topic)
    elif "configuração" in topic:
        return realizar_configuracao(query)
    elif any(word in topic for word in ["finalizar", "xau", "tchau", "adeus", "até logo", "ate logo", "encerrar", "terminar"]):
        return finalizar_atendimento(query)
    else:
        return outros_casos(query)
    
def realizar_cadastro(query, topic):
    try:
        # First get the initial response
        initial_response = iniciar_cadastro_chain.invoke({
            "query": query,
            "format_instructions": format_instructions
        })
        user_input = input(initial_response.content + "\n")
        
        max_attempts = 5  # Prevent infinite loops
        attempt_count = 0
        
        while attempt_count < max_attempts:
            try:
                # Get the JSON data
                json_data = construtor_JSON_cadastro_chain.invoke({
                    "query": user_input,
                    "format_instructions": format_instructions
                })
                print(json_data)
                
                # Verify if JSON is complete
                json_status = verificar_JSON_chain.invoke({
                    "json_data": json_data
                })
                print(json_status)
                
                if json_status == "completo":
                    return f"{initial_response}\n\nDados extraídos: {json_data}", False
                
                # If incomplete, ask for missing data
                print("\nPor favor, forneça os dados que estão faltando.")
                user_input = input("Digite os dados complementares: ")
                # Concatenate new input with previous data to maintain context
                user_input = f"{user_input} {json_data}"
                
                attempt_count += 1
                
                if attempt_count == max_attempts:
                    return "Número máximo de tentativas atingido. Por favor, inicie o cadastro novamente.", False
                    
            except Exception as e:
                print(f"Erro ao processar os dados: {str(e)}")
                return "Ocorreu um erro ao processar os dados. Por favor, tente novamente.", False
                
    except KeyboardInterrupt:
        return "Operação cancelada pelo usuário.", False
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return "Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.", False

def realizar_configuracao(query):
    response_chain = configuracao_chain
    response = response_chain.invoke({
        "query": query,
        "format_instructions": format_instructions
    })
    print(response.content)
    return response, False
    
def finalizar_atendimento(query):
    response_chain = finalizar_chain
    response = response_chain.invoke({
        "query": query,
        "format_instructions": format_instructions
    })
    print(response.content)
    return response, True

def outros_casos(query):
    response_chain = nao_se_aplica_chain
    response = response_chain.invoke({
        "query": query,
        "format_instructions": format_instructions
    })
    print(response.content)
    return response, False

# Main conversation loop
end_conversation = False
while not end_conversation:
    query = input("Como posso ajudar? ")
    classification = chain.invoke({"query": query})
    print(classification)

    response, end_conversation = route({
        "topic": classification,
        "query": query
    })

    