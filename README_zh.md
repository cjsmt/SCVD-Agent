# Smart Contracts Vulnerability Detection Tool

## 项目简介

该项目是一个智能合约漏洞检测工具，旨在通过机器学习和知识库检索技术，帮助开发者识别和修复智能合约中的潜在漏洞。该工具支持上传智能合约代码，并提供基准测试功能，以评估模型的准确性。

## 功能

- **智能合约上传**：支持上传 `.sol` 格式的智能合约文件。
- **漏洞检测**：通过集成的 RAG（Retrieval-Augmented Generation）模型，自动检测合约中的漏洞。
- **基准测试**：支持对上传的合约进行基准测试，评估模型的准确率。
- **知识库查询**：在检测过程中，可以选择是否查阅 RAG 知识库以提高检测准确性。

## 技术栈

- Python
- Streamlit
- Langchain
- PyPDF2
- FAISS
- DashScope

## 安装

1. 克隆该项目：

   ```bash
   git clone https://github.com/yourusername/SCVD-Agent.git
   cd SCVD-Agent
   ```

2. 创建并激活虚拟环境：
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # 在 macOS/Linux 上
   venv\Scripts\activate  # 在 Windows 上
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 设置环境变量：
   创建一个 .env 文件，并添加以下内容：
   ```bash
   DASHSCOPE_API_KEY=your_dashscope_api_key
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

## 使用

1. 启动应用：
   ```bash
   streamlit run main.py
   ```
2. 在浏览器中打开 http://localhost:8501。

3. 上传智能合约文件并输入问题，点击提交以获取检测结果。

4. 使用基准测试功能，上传多个合约文件并选择其标签（安全或有漏洞），以评估模型的准确性。
