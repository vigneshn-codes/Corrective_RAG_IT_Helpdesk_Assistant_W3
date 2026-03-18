import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_text_splitters import RecursiveCharacterTextSplitter

app = FastAPI()

# Configuration - Replace with your Tavily Key
os.environ["TAVILY_API_KEY"] = "your_tavilly_apikey"

# 1. Setup Local Vector DB
loader = PyPDFLoader("it_docs.pdf")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
retriever = vectorstore.as_retriever()

# 2. Setup LLM (Ollama)
llm = ChatOllama(model="llama3.2", temperature=0)

class Query(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_helpdesk(query: Query):
    # Step A: Retrieve Internal Docs
    docs = retriever.invoke(query.prompt)
    context = "\n".join([d.page_content for d in docs])

    # DEBUG: See what was actually found in the logs
    print(f"--- RETRIEVED CONTEXT ---\n{context}\n-------------------------")
    
    # Step B: Grading (The "Corrective" part)
    # Simple logic: If LLM thinks context is irrelevant, it triggers search
    grade_prompt = (
        f"USER QUERY: {query.prompt}\n"
        f"RETRIEVED CONTEXT: {context}\n\n"
        "SYSTEM TASK: Does the context above contain information that helps answer the user query?\n"
        "If it mentions the same technical issue (even if the solution is brief), output 'YES'.\n"
        "If it is completely unrelated, output 'NO'.\n"
        "Output ONLY the word 'YES' or 'NO':"
    )
    grade = llm.invoke(grade_prompt).content.strip().upper()


    print(f"--- GRADER DECISION: {grade} ---")

    if "NO" in grade:
        # Step C: Fallback to External Search (StackOverflow/Vendor Notes)
        search = TavilySearchResults(k=3)
        external_data = search.run(f"IT Helpdesk: {query.prompt}")
        source = "External (Tavily/StackOverflow)"
        final_context = external_data
    else:
        source = "Internal Documentation"
        final_context = context

    # Step D: Final Answer
    final_prompt = f"Using this context: {final_context}, answer the user: {query.prompt}"
    response = llm.invoke(final_prompt)
    
    return {"answer": response.content, "source": source}