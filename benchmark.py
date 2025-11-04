import glob
import streamlit as st
from agent import get_conversational_chain, get_answer_with_rag

# 基准测试功能
def benchmark_contracts(check_rag):
    contracts = []
    # 从本地 test_dataset 目录读取合约代码
    safe_contracts = glob.glob("test_dataset/safe/*.sol")
    vulnerable_contracts = glob.glob("test_dataset/vulnerable/*.sol")

    # 将安全和有漏洞的合约添加到 contracts 列表
    for contract in safe_contracts:
        with open(contract, 'r') as file:
            contracts.append({"code": file.read(), "label": "无漏洞"})
    
    for contract in vulnerable_contracts:
        with open(contract, 'r') as file:
            contracts.append({"code": file.read(), "label": "有漏洞"})

    correct_predictions = 0
    total_contracts = len(contracts)

    for contract in contracts:
        user_question = "这个合约是否有漏洞？你的答复只需要回复”有漏洞“或”无漏洞“。"
        contract_code = contract["code"]

        # 如果选择查阅RAG知识库
        if check_rag:
            # 调用RAG知识库进行预测
            response = get_answer_with_rag(user_question, contract_code)
        else:
            # 直接进行预测
            response = get_conversational_chain(None, user_question, contract_code)

        prediction = "有漏洞" if "漏洞" in response['output'] else "无漏洞"
        st.write(f"Contract Prediction: {prediction}, Actual Label: {contract['label']}")
        if prediction == contract["label"]:
            correct_predictions += 1

    accuracy = correct_predictions / total_contracts * 100 if total_contracts > 0 else 0
    return accuracy

