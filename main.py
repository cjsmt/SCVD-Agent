import streamlit as st
import os
from rag import pdf_read, get_chunks, vector_store, check_database_exists
from benchmark import benchmark_contracts
from agent import get_answer_with_rag

# 检查目录是否非空
def is_directory_non_empty(directory):
    return any(os.scandir(directory))

# 前端网页界面
def main():
    st.set_page_config("Smart Contracts Vulnerability Detection tool", layout="wide")
    st.header("Smart Contracts Vulnerability Detection tool")
    
    # 显示数据库状态
    if check_database_exists():
        pass
    else:
        st.warning("⚠️ Please upload and process PDF files to create the database.")

    # Drag and drop upload box
    contract_code = st.file_uploader("📜 Upload your Smart Contract:", type=["sol"], accept_multiple_files=False, help="Drag and drop or click to upload smart contract files (.sol)")

    user_question = st.text_input("💬 Your question:", 
                                placeholder="Enter your question about the uploaded smart contract...",
                                disabled=not check_database_exists())

    # Submit button
    if st.button("Submit", disabled=not check_database_exists()):
        if user_question and contract_code:
            with st.spinner("🤔 AI is analyzing the document..."):
                try:
                    response = get_answer_with_rag(user_question, contract_code.read().decode("utf-8"))  # Read file content and decode to string
                    st.write("🤖 Answer: ", response['output'])
                except Exception as e:
                    st.error(f"❌ Error loading database: {str(e)}")
                    st.info("💡 Please reprocess the PDF file")
        else:
            st.error("❌ Please ensure you have entered a question and uploaded the smart contract code!")

    # 基准测试部分
    st.markdown("---")
    st.header("Benchmark Testing for Smart Contract Vulnerability Detection")
    
    # 添加复选框，询问是否为有漏洞的合约
    is_vulnerable = st.checkbox("所有上传的合约是否为有漏洞的合约？", value=False)
    
    # Upload multiple smart contract files
    uploaded_contracts = st.file_uploader("📂 Upload smart contract files (.sol)", type=["sol"], accept_multiple_files=True)
    if uploaded_contracts and st.button("Upload"):
        save_dir = f"test_dataset/{'vulnerable' if is_vulnerable else 'safe'}"
        os.makedirs(save_dir, exist_ok=True)  # 确保目录存在
        for uploaded_file in uploaded_contracts:
            save_path = os.path.join(save_dir, uploaded_file.name)
            contract_code = uploaded_file.read().decode("utf-8")
            with open(save_path, "w") as f:
                f.write(contract_code)
        st.success(f"Files have been saved to {save_dir}")

    check_rag = st.checkbox("Consult RAG knowledge base during benchmark testing", value=True)
    
    if st.button("Start Benchmark Testing"):
        # Check if both directories are non-empty
        safe_non_empty = is_directory_non_empty("test_dataset/safe")
        vulnerable_non_empty = is_directory_non_empty("test_dataset/vulnerable")

        if safe_non_empty or vulnerable_non_empty:
            accuracy = benchmark_contracts(check_rag)
            st.success(f"Benchmark testing completed! Accuracy: {accuracy:.2f}%")
        else:
            st.warning("⚠️ Please ensure at least one directory (safe or vulnerable) contains contract files for benchmark testing.")

    # 侧边栏
    with st.sidebar:
        st.title("📁 File Management")
        
        # 显示当前状态
        if check_database_exists():
            st.success("✅ Database Status: Ready")
        else:
            st.info("📝 Status: Waiting for uploading PDF.")

        if st.button("🗑️ Clear Database"):
            try:
                import shutil
                if os.path.exists("faiss_db"):
                    shutil.rmtree("faiss_db")
                st.success("Database has been cleared")
                st.rerun()
            except Exception as e:
                st.error(f"Clear failed: {e}")
        
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
            "🚀 Submit and Process", 
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
                        
                        st.success("✅ Finish Processing! Now you can start asking questions.")
                        st.balloons()
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ An error occurred while processing the PDF: {str(e)}")
            else:
                st.warning("⚠️ Please upload at least one PDF file before processing.")

if __name__ == "__main__":
    main()


