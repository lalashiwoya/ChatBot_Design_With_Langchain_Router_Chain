
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from utils import init_llm, init_memory, convert_memory_to_str
from llama_index.core import Settings
from api.full_chain import init_full_chain
from langchain.schema.runnable.config import RunnableConfig

MAX_TOKEN_LIMIT = 500

@cl.on_chat_start
async def on_chat_start():
    llm = init_llm()
    memory = init_memory(llm, max_token_limit=MAX_TOKEN_LIMIT)
    full_chain = init_full_chain(llm)
    cl.user_session.set("full_chain", full_chain)
    cl.user_session.set("memory", memory)

@cl.on_message
async def on_message(message: cl.Message):
    full_chain = cl.user_session.get("full_chain")
    memory = cl.user_session.get("memory")
    elements = []
    actions = []
    res = cl.Message(content="", elements=elements, actions=actions)
    
    async for chunk in full_chain.astream(
        {
            "question": message.content,
            "memory": convert_memory_to_str(memory),
             
        },
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        # response.append(chunk)
        await res.stream_token(chunk)
    await res.send()
    # memory.chat_memory.add_user_message(message.content)
    # memory.chat_memory.add_ai_message(res.content)
    memory.save_context({"input": message.content}, {"output": res.content})
    
    
 