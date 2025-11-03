import streamlit as st
import os
from rag import pdf_read, get_chunks, vector_store, check_database_exists
from benchmark import benchmark_contracts
from agent import get_answer_with_rag

# 前端网页界面
def main():
    st.set_page_config("Smart Contracts Vulnerability Detection tool", layout="wide")
    st.header("Smart Contracts Vulnerability Detection tool")
    
    # 显示数据库状态
    if check_database_exists():
        pass
    else:
        st.warning("⚠️ Please upload and process PDF files to create the database.")

    # 拖拽上传框
    contract_code = st.file_uploader("📜 Upload your Smart Contract :", type=["sol"], accept_multiple_files=False, help="拖拽或点击上传智能合约文件（.sol）")

    user_question = st.text_input("💬 Your question:", 
                                placeholder="Enter your question about the uploaded smart contract...",
                                disabled=not check_database_exists())

    # 提交按钮
    if st.button("提交", disabled=not check_database_exists()):
        if user_question and contract_code:
            with st.spinner("🤔 AI正在分析文档..."):
                try:
                    response = get_answer_with_rag(user_question, contract_code.read().decode("utf-8"))  # 读取文件内容并解码为字符串
                    st.write("🤖 回答: ", response)
                except Exception as e:
                    st.error(f"❌ 加载数据库时出错: {str(e)}")
                    st.info("💡 请重新处理PDF文件")
        else:
            st.error("❌ 请确保输入问题和上传智能合约代码！")

    # 基准测试部分
    st.markdown("---")
    st.header("基准测试")
    
    # 添加复选框，询问是否为有漏洞的合约
    is_vulnerable = st.checkbox("所有上传的合约是否为有漏洞的合约？", value=False)
    
    # 上传多个智能合约文件
    uploaded_contracts = st.file_uploader("📂 上传智能合约文件（.sol）", type=["sol"], accept_multiple_files=True)
    
    contracts = []
    
    if uploaded_contracts:
        for uploaded_file in uploaded_contracts:
            # 读取文件内容
            contract_code = uploaded_file.read().decode("utf-8")
            # 根据复选框状态自动附上标签
            label = "有漏洞" if is_vulnerable else "无漏洞"
            contracts.append({"code": contract_code, "label": label})

    check_rag = st.checkbox("在基准测试中查阅RAG知识库", value=True)
    
    if st.button("开始基准测试"):
        if contracts:
            accuracy = benchmark_contracts(check_rag, contracts)
            st.success(f"基准测试完成！准确率: {accuracy:.2f}%")
        else:
            st.warning("⚠️ 请上传至少一个智能合约文件进行基准测试。")

    # 侧边栏
    with st.sidebar:
        st.title("📁 File Management")
        
        # 显示当前状态
        if check_database_exists():
            st.success("✅ Database Status：Ready")
        else:
            st.info("📝 Status: Waiting for uploading PDF.")

        if st.button("🗑️ Clear Database"):
            try:
                import shutil
                if os.path.exists("faiss_db"):
                    shutil.rmtree("faiss_db")
                st.success("数据库已清除")
                st.rerun()
            except Exception as e:
                st.error(f"清除失败: {e}")
        
        st.markdown("---")
        
        # 文件上传
        pdf_doc = st.file_uploader(
            "📎 Upload PDF", 
            accept_multiple_files=True,
            type=['pdf'],
            help="Upload one or more PDF files for processing"
        )
        
        if pdf_doc:
            st.info(f"📄 {len(pdf_doc)} files have been chosen")
            for i, pdf in enumerate(pdf_doc, 1):
                st.write(f"{i}. {pdf.name}")
        
        # 处理按钮
        process_button = st.button(
            "🚀 submit and process", 
            disabled=not pdf_doc,
            use_container_width=True
        )
        
        if process_button:
            if pdf_doc:
                with st.spinner("📊 Processing PDF files..."):
                    try:
                        # 读取PDF内容
                        raw_text = pdf_read(pdf_doc)
                        
                        if not raw_text.strip():
                            st.error("❌ The uploaded PDF file is empty or its content cannot be read. Please check the file and upload it again.")
                            return
                        
                        # 分割文本
                        text_chunks = get_chunks(raw_text)
                        st.info(f"📝 The text has been divided into {len(text_chunks)} segments")
                        
                        # 创建向量数据库
                        vector_store(text_chunks)
                        
                        st.success("✅ Finish Processing! Now You can start asking questions.")
                        st.balloons()
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ An error occurred while processing the PDF: {str(e)}")
            else:
                st.warning("⚠️ Please upload at least one PDF file before processing.")

if __name__ == "__main__":
    main()


