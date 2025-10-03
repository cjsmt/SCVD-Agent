import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
from rag import embeddings, pdf_read, get_chunks, vector_store, check_database_exists
from agent import get_conversational_chain

# 7. 用户提问逻辑（调用FAISS）
def user_input(user_question):
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
        get_conversational_chain(retrieval_chain, user_question)
        
    except Exception as e:
        st.error(f"❌ 加载数据库时出错: {str(e)}")
        st.info("请重新处理PDF文件")


# 前端网页界面
def main():
    st.set_page_config("🤖 智能合约安全漏洞检测工具")
    st.header("🤖 智能合约安全漏洞检测工具")
    
    # 显示数据库状态
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if check_database_exists():
            pass
        else:
            st.warning("⚠️ 请先上传并处理PDF文件")
    
    with col2:
        if st.button("🗑️ 清除数据库"):
            try:
                import shutil
                if os.path.exists("faiss_db"):
                    shutil.rmtree("faiss_db")
                st.success("数据库已清除")
                st.rerun()
            except Exception as e:
                st.error(f"清除失败: {e}")

    # 用户问题输入
    user_question = st.text_input("💬 请输入问题", 
                                placeholder="例如：这个文档的主要内容是什么？",
                                disabled=not check_database_exists())

    if user_question:
        if check_database_exists():
            with st.spinner("🤔 AI正在分析文档..."):
                user_input(user_question)
        else:
            st.error("❌ 请先上传并处理PDF文件！")

    # 侧边栏
    with st.sidebar:
        st.title("📁 文档管理")
        
        # 显示当前状态
        if check_database_exists():
            st.success("✅ 数据库状态：已就绪")
        else:
            st.info("📝 状态：等待上传PDF")
        
        st.markdown("---")
        
        # 文件上传
        pdf_doc = st.file_uploader(
            "📎 上传PDF文件", 
            accept_multiple_files=True,
            type=['pdf'],
            help="支持上传多个PDF文件"
        )
        
        if pdf_doc:
            st.info(f"📄 已选择 {len(pdf_doc)} 个文件")
            for i, pdf in enumerate(pdf_doc, 1):
                st.write(f"{i}. {pdf.name}")
        
        # 处理按钮
        process_button = st.button(
            "🚀 提交并处理", 
            disabled=not pdf_doc,
            use_container_width=True
        )
        
        if process_button:
            if pdf_doc:
                with st.spinner("📊 正在处理PDF文件..."):
                    try:
                        # 读取PDF内容
                        raw_text = pdf_read(pdf_doc)
                        
                        if not raw_text.strip():
                            st.error("❌ 无法从PDF中提取文本，请检查文件是否有效")
                            return
                        
                        # 分割文本
                        text_chunks = get_chunks(raw_text)
                        st.info(f"📝 文本已分割为 {len(text_chunks)} 个片段")
                        
                        # 创建向量数据库
                        vector_store(text_chunks)
                        
                        st.success("✅ PDF处理完成！现在可以开始提问了")
                        st.balloons()
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ 处理PDF时出错: {str(e)}")
            else:
                st.warning("⚠️ 请先选择PDF文件")
        
        # 使用说明
        with st.expander("💡 使用说明"):
            st.markdown("""
            **步骤：**
            1. 📎 上传一个或多个PDF文件
            2. 🚀 点击"Submit & Process"处理文档
            3. 💬 在主页面输入您的问题
            4. 🤖 AI将基于PDF内容回答问题
            
            **提示：**
            - 支持多个PDF文件同时上传
            - 处理大文件可能需要一些时间
            - 可以随时清除数据库重新开始
            """)

if __name__ == "__main__":
    main()


