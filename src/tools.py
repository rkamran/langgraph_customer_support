from langchain_core.language_models import BaseChatModel
from langchain.chat_models import init_chat_model
import logging
import os
import sys


from dotenv import load_dotenv
load_dotenv()

def get_logger(name: str, level=logging.INFO):    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name) 
    logger.addHandler(stream_handler)
    logger.setLevel(level)    
    
    return logger

logger = get_logger(__name__)


def get_llm(model_name: str, temperature: float = 0) -> BaseChatModel:
    return init_chat_model(
        model=f"ollama:{model_name}", 
        base_url=f'{os.getenv("OLLAMA_BASE_URL")}', 
        temperature=temperature
    )


        