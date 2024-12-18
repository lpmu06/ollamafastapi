from fastapi import FastAPI, Response
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv(find_dotenv())

app = FastAPI()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_cadastro = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define response schemas and parsers
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

# Define chains
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

# Define other chains (same as teste3.py)
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

# ... other chain definitions from teste3.py ...

@app.get("/ask")
async def ask(prompt: str):
    try:
        # Get classification
        classification = chain.invoke({"query": prompt})
        
        # Process based on classification
        topic = classification.lower()
        response = None
        end_conversation = False
        
        if "cadastro" in topic:
            # For cadastro, we'll return the initial guidance
            response = iniciar_cadastro_chain.invoke({
                "query": prompt,
                "format_instructions": format_instructions
            })
            
            # If user provided data, try to process it
            json_data = construtor_JSON_cadastro_chain.invoke({
                "query": prompt,
                "format_instructions": format_instructions
            })
            
            return {
                "type": "cadastro",
                "message": response.content,
                "data": json_data if json_data else None
            }
            
        elif "configuração" in topic:
            response = configuracao_chain.invoke({
                "query": prompt,
                "format_instructions": format_instructions
            })
            return {
                "type": "configuracao",
                "message": response.content
            }
            
        elif any(word in topic for word in ["finalizar", "xau", "tchau", "adeus", "até logo", "ate logo", "encerrar", "terminar"]):
            response = finalizar_chain.invoke({
                "query": prompt,
                "format_instructions": format_instructions
            })
            return {
                "type": "finalizar",
                "message": response.content,
                "end_conversation": True
            }
            
        else:
            response = nao_se_aplica_chain.invoke({
                "query": prompt,
                "format_instructions": format_instructions
            })
            return {
                "type": "outros",
                "message": response.content
            }

    except Exception as e:
        return {"error": str(e)}
