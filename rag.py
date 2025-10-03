import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

load_dotenv(override=True)
DashScope_API_KEY = os.environ.get("DASHSCOPE_API_KEY")
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# 3. 初始化向量Embedding模型
embeddings = DashScopeEmbeddings(model="text-embedding-v1", dashscope_api_key=DashScope_API_KEY)

# 4. 处理PDF文件，并向量化
# 4.1. 逐页读取PDF内容并拼接
def pdf_read(pdf_doc):
    text = ""
    for pdf in pdf_doc:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# 4.2. 将长文本切片为多个段落（chunk），每段1000字，重叠200字
def get_chunks(text):
    text_spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_spliter.split_text(text=text)
    return chunks

# 4.3. 用FAISS建立向量索引，并保存到本地faiss_db/
def vector_store(text_chunk):
    vector_store = FAISS.from_texts(texts=text_chunk, embedding=embeddings)
    vector_store.save_local("faiss_db")


# 6. 检查FAISS数据库是否存在，检查本地是否已有向量化的数据
def check_database_exists():
    return os.path.exists("faiss_db") and os.path.exists("faiss_db/index.faiss")