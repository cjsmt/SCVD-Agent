import os
import streamlit as st
from rag import check_database_exists, embeddings
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_community.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
from dotenv import load_dotenv
load_dotenv(override=True)

# 5. Agent对话链 + 工具调用（核心RAG）
DeepSeek_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

def get_conversational_chain(tools, ques, contract_code):
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

    if tools is None:
        tool = []
    else:
        tool = [tools]
    agent = create_tool_calling_agent(llm, tool, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tool, verbose=True)

    full_input = f"合约代码：\n{contract_code}\n\n问题：{ques}"
    response = agent_executor.invoke({"input": full_input})
    return response

# 7. 用户提问逻辑（调用FAISS）
def get_answer_with_rag(user_question, contract_code):
    if not check_database_exists():
        raise Exception("FAISS数据库不存在")
    # 加载FAISS数据库
    new_db = FAISS.load_local("faiss_db", embeddings, allow_dangerous_deserialization=True)
        
    # 构建retriever工具
    retriever = new_db.as_retriever()
    retrieval_chain = create_retriever_tool(retriever, "pdf_extractor", "This tool is to give answer to queries from the pdf")
    
    # 调用对话链
    response = get_conversational_chain(retrieval_chain, user_question, contract_code)
    return response
