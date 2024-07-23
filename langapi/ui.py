from dotenv import load_dotenv

load_dotenv()

from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
import streamlit as st

st_callback = StreamlitCallbackHandler(st.container())

from langchain_mongodb.cache import MongoDBCache
from langchain_core.globals import set_llm_cache

set_llm_cache(MongoDBCache(
    connection_string = "mongodb://root:example@localhost:27017",
    collection_name = "test_cache",
    database_name = "langchain_llm_cache",
))

import streamlit as st
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.agent_toolkits.load_tools import load_tools

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Help the user interface with a search engine.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


# from langchain_experimental.llms.ollama_functions import OllamaFunctions
# llm = OllamaFunctions(base_url="http://localhost:11434", temperature=0, num_ctx=32768, streaming=True, model="mistral", format="json")
from langchain_ollama import ChatOllama
llm = ChatOllama(base_url="http://localhost:11434", temperature=0, num_ctx=32768, streaming=True, model="mistral")
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(temperature=0, streaming=True, model="gpt-4o-mini")
tools = load_tools(["ddg-search"])
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory



from langchain_core.runnables.history import RunnableWithMessageHistory

chain_with_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string="mongodb://root:example@localhost:27017",
        database_name="langchain_chat_history_cache",
        collection_name="test_chat_histories",
    ),
    input_messages_key="input",
    history_messages_key="history",
)

config = {}

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = chain_with_history.invoke(
            {"input": prompt}, {"callbacks": [st_callback], "configurable": {"session_id": "test_session"}}
        )
        st.write(response["output"])