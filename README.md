🍳 Collective RAG: IT Helpdesk Assistant
===================================

**IT Helpdesk Assistant RAG**  A local, privacy-first IT Helpdesk assistant built using the **Corrective Retrieval-Augmented Generation (CRAG)** architecture. This application intelligently decides whether to trust internal documentation or fall back to external web searches (StackOverflow/Vendor Notes) to answer technical queries.

## 🚀 Key Features
- **Local LLM:** Powered by **Ollama (Llama 3)** for data privacy.
- **Self-Correction Logic:** Evaluates retrieved documents for relevance before answering.
- **Intelligent Fallback:** Uses **Tavily Search API** if internal documentation is missing or irrelevant.
- **FastAPI Backend:** High-performance asynchronous API.
- **Streamlit UI:** Clean, user-friendly chat interface.

---

## 🏗️ Architecture
1. **Ingestion:** Converts a `knowledge.json` of internal IT tickets into a searchable PDF.
2. **Retrieval:** Uses **ChromaDB** (or FAISS) and **nomic-embed-text** to find relevant local docs.
3. **Grading:** The LLM acts as a "Quality Grader" to verify if the retrieved context actually answers the user's problem.
4. **Correction:** - **Match:** Use internal docs for the final answer.
   - **No Match:** Trigger an external search to find a solution online.

---
## 🛠️ Setup & Installation

### 1. Prerequisites
- **Python 3.11 or 3.12** (Recommended for AI library stability)
- **Ollama** installed and running.
- **Tavily API Key** (Get one at [tavily.com](https://tavily.com/))

### 2. Install Dependencies
```bash
pip install fastapi uvicorn streamlit langchain langchain-community \
langchain-ollama langchain-tavily chromadb pypdf fpdf
```

### 3. Setup Models

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   ollama pull llama3  ollama pull nomic-embed-text   `

### 4\. Prepare Local Data

Update knowledge.json with your IT issues, then generate the vector database:

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python ingest.py   `

🚦 Running the App
------------------

### Step 1: Start the Backend (FastAPI)

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   export TAVILY_API_KEY='your_api_key'  uvicorn main:app --reload   `

### Step 2: Start the Frontend (Streamlit)

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   streamlit run app.py   `

📁 Project Structure
--------------------

*   main.py: FastAPI server containing the CRAG logic and retriever.
    
*   app.py: Streamlit interface for user interaction.
    
*   ingest.py: Script to convert JSON documentation into a PDF/Vector DB.
    
*   knowledge.json: Your internal IT helpdesk data.
    

📝 Example
----------

*   **Query:** _"VPN Connection Timeout"_ - **Action:** Found in local docs → **Source: Internal Documentation**
    
*   **Query:** _"How to fix blue screen error on Windows 12?"_ - **Action:** Not in local docs → **Source: External (Tavily Search)**
    

⚖️ Author
---------

_Vignesh Nagarajan - AI Engineer_