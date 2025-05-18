from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def load_llm(model_name: str):
    """ Load LLM from either OpenAI or Google Gemini """

    if model_name in ["gpt-3.5-turbo", "gpt-4o"]:
        llm = ChatOpenAI(
            model=model_name,
            temperature=0.0,
            max_tokens=1000
        )
    
    elif model_name == "gemini-2.0-flash":
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")  # hoặc hardcode nếu cần

        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.0
        )

    else:
        raise ValueError(
            f"Model {model_name} not supported. \
             Please choose from: gpt-3.5-turbo, gpt-4o, gemini-pro"
        )
    
    return llm
