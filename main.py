import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
from rag import embeddings, pdf_read, get_chunks, vector_store, check_database_exists
from agent import get_conversational_chain

# 7. 用户提问逻辑（调用FAISS）
def user_input(user_question, contract_code):
    # 检查数据库是否存在
    if not check_database_exists():
        st.error("❌ 请先上传PDF文件并点击'Submit & Process'按钮来处理文档！")
        st.info("💡 步骤：1️⃣ 上传PDF → 2️⃣ 点击处理 → 3️⃣ 开始提问")
        return
    
    try:
        # 加载FAISS数据库
        new_db = FAISS.load_local("faiss_db", embeddings, allow_dangerous_deserialization=True)
        
        # 构建retriever工具
        retriever = new_db.as_retriever()
        retrieval_chain = create_retriever_tool(retriever, "pdf_extractor", "This tool is to give answer to queries from the pdf")
        
        # 调用对话链
        response = get_conversational_chain(retrieval_chain, user_question, contract_code)
        st.write("🤖 回答: ", response)
        
    except Exception as e:
        st.error(f"❌ 加载数据库时出错: {str(e)}")
        st.info("请重新处理PDF文件")


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
                user_input(user_question, contract_code.read().decode("utf-8"))  # 读取文件内容并解码为字符串
        else:
            st.error("❌ 请确保输入问题和上传智能合约代码！")

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


