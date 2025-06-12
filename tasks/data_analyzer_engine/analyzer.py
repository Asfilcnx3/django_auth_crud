from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType
import pandas as pd
import os

# Create the function that allows to read csv, excel or json
def load_files(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext == '.csv':
        try:
            df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file_path, encoding='latin_1', on_bad_lines='skip')
            except:
                df = pd.read_csv(file_path, encoding='iso-8859-1', on_bad_lines='skip')
    elif ext == '.xlsx':
        df = pd.read_excel(file_path)
    elif ext == '.json':
        df = pd.read_json(file_path)
    else:
        raise ValueError('File Type not supported')
    return df

def df_analyzer(file_path, query, historial=None):
    try:
        df = load_files(file_path)

        # Valid the DF size
        if df.shape[0] > 10000 or df.shape[1] > 50:
            return "El archivo es demasiado grande. Por favor usa un archivo más pequeño.", historial

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "No se encontró la API Key. Define GOOGLE_API_KEY como variable de entorno.", historial

        llm = ChatGoogleGenerativeAI(
            model = "gemini-2.0-flash-exp",
            google_api_key = api_key,
            temperature = 0,
            disable_streaming = True
        )

        agent = create_pandas_dataframe_agent(
            llm = llm,
            df = df,
            verbose = False,
            agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            return_intermediate_steps = False,
            allow_dangerous_code = True
        )

        print("Executing agent whit query:", query)
        raw_answer = agent.invoke(query)
        user_answer = raw_answer.get("output", "No output from the model.")

        if historial is not None:
            historial.append(f"**Question:** {query}\n**Answer:** {user_answer}")
            return user_answer, historial

        return user_answer

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        if historial is not None:
            historial.append(error_msg)
            return error_msg, historial
        return error_msg
    

#### Test
# # Create the analyzer with model and query
# def df_analyzer(file_path, query, historial=None):
#     df = load_files(file_path)

#     llm = ChatGoogleGenerativeAI(
#         model = "gemini-2.0-flash-exp",
#         google_api_key = os.getenv("GOOGLE_API_KEY"),
#         temperature = 0,
#         disable_streaming = True 
#     )

#     agent = create_pandas_dataframe_agent(
#         llm = llm,
#         df = df,
#         verbose = False,
#         agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         return_intermediate_steps = False,
#         allow_dangerous_code = True
#     )

#     raw_answer = agent.invoke(query)
#     user_answer = raw_answer['output']

#     if historial is not None:
#         historial.append(f"**Pregunta:** {query}\n**Respuesta:** {user_answer}")
#         return user_answer, historial
#     return user_answer

# print(df_analyzer(r'C:\Users\sosbr\Documents\django-crud-auth\tmp\GDP-Dataset.xlsx', 'What is the GDP from albania in 2005?'))