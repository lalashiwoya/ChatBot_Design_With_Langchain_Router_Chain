from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain_core.memory import BaseMemory
from langchain.chat_models.base import  BaseChatModel

def init_llm():
    llm = ChatOpenAI(temperature=0, model_name = "gpt-3.5-turbo", streaming = True)
    return llm

def init_memory(llm: BaseChatModel, max_token_limit:int = 500):
    # memory = ConversationBufferMemory(return_messages = True)
    memory = ConversationSummaryBufferMemory(return_messages = True,
                                            max_token_limit= max_token_limit,
                                            llm = llm)
    return memory
    


def convert_memory_to_str(memory: BaseMemory) -> str:
    return str(memory.load_memory_variables({})['history'])