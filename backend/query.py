from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_together import Together

CHROMA_PATH = "chroma"

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"
TOGETHER_MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

db = Chroma(persist_directory=CHROMA_PATH, embedding_function=SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME))
llm = Together(model=TOGETHER_MODEL_NAME, temperature=0.7, max_tokens=200)

def generate_response(query_text):
    results = db.similarity_search(query_text, k=3)
    if not results:
        return "No sources found on Encyclopedia Galactica."

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    
    prompt = (
        "Use the following sources to answer the question:\n\n"
        f"{context_text}\n\n"
        "Question: {query_text}."
    )
    
    response_text = llm.invoke(prompt)

    return f"{response_text}\n\nSources:\n{context_text}"
