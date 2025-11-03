from langchain_community.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
from rag import embeddings
from agent import get_conversational_chain, get_answer_with_rag

# 基准测试功能
def benchmark_contracts(check_rag, contracts):
    correct_predictions = 0
    total_contracts = len(contracts)

    for contract in contracts:
        user_question = "这个合约是否有漏洞？"
        contract_code = contract["code"]

        # 如果选择查阅RAG知识库
        if check_rag:
            # 调用RAG知识库进行预测
            response = get_answer_with_rag(user_question, contract_code)
        else:
            # 直接进行预测
            response = get_conversational_chain(None, user_question, contract_code)

        prediction = "有漏洞" if "漏洞" in response else "无漏洞"

        if prediction == contract["label"]:
            correct_predictions += 1

    accuracy = correct_predictions / total_contracts * 100 if total_contracts > 0 else 0
    return accuracy
    
