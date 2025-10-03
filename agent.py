import os
import streamlit as st
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv(override=True)

# 5. Agent对话链 + 工具调用（核心RAG）
DeepSeek_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

def get_conversational_chain(tools, ques):
    llm = init_chat_model("deepseek-chat", model_provider="deepseek")
    prompt = ChatPromptTemplate.from_messages([
        (
            "system", 
            """你是AI助手，请根据提供的上下文回答问题，确保提供所有细节，如果答案不在上下文中，请说"答案不在上下文中"，不要提供错误的答案"""
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    tool = [tools]
    agent = create_tool_calling_agent(llm, tool, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tool, verbose=True)

    response = agent_executor.invoke({"input": ques})
    print(response)
    st.write("🤖 回答: ", response['output'])