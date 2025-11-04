# Smart Contracts Vulnerability Detection Tool

## Project Overview

This project is a smart contract vulnerability detection tool designed to help developers identify and fix potential vulnerabilities in smart contracts using machine learning and knowledge retrieval techniques. The tool supports uploading smart contract code and provides benchmarking functionality to evaluate the accuracy of the model.

## Features

- **Smart Contract Upload**: Supports uploading smart contract files in `.sol` format.
- **Vulnerability Detection**: Automatically detects vulnerabilities in contracts using the integrated RAG (Retrieval-Augmented Generation) model.
- **Benchmark Testing**: Supports benchmarking the uploaded contracts to evaluate the accuracy of the model.
- **Knowledge Base Query**: During detection, users can choose to consult the RAG knowledge base to improve detection accuracy.

## Tech Stack

- Python
- Streamlit
- Langchain
- PyPDF2
- FAISS
- DashScope

## Installation

1. Clone the project:

   ```bash
   git clone https://github.com/yourusername/SCVD-Agent.git
   cd SCVD-Agent
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables: Create a .env file and add the following content:
   ```bash
   DASHSCOPE_API_KEY=your_dashscope_api_key
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

## Usage
1. Start the application:
   ```bash
   streamlit run main.py
   ```

2. Open your browser and navigate to http://localhost:8501.

3. Upload smart contract files and enter your questions, then click submit to get the detection results.

4. Use the benchmark testing feature to upload multiple contract files and select their labels (safe or vulnerable) to evaluate the model's accuracy.