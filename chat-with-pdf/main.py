from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import hashlib

from openai import OpenAI

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

loader = PyPDFLoader("./chat-with-pdf/files/embeddings & vector stores.pdf")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)


def chunk_id(chunk):
    key = f"{chunk.metadata['source']}|{chunk.metadata['page']}|{chunk.page_content}"
    return hashlib.sha256(key.encode()).hexdigest()


ids = [chunk_id(chunk) for chunk in chunks]
vector_store.add_documents(documents=chunks, ids=ids)


def get_results(user_query):
    results = vector_store.similarity_search(
        user_query,
        k=3,
    )
    return results

def get_chunk_template(chunk):
    return f"<Chunk>\n{chunk.page_content}\n</Chunk>" 

def get_prompt(user_query, results):
    return f"""You are a helpful assistant that answers questions using only the context provided.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
<Context>
{"\n".join([get_chunk_template(chunk) for chunk in results])}
</Context>
<Question>
{user_query}
</Question>
"""
client = OpenAI()

while True:
    user_query = input("Enter your question (or 'exit' to quit): ")
    if user_query.lower() == 'exit':
        break

    results = get_results(user_query)
    PROMPT = get_prompt(user_query, results)
    response = client.responses.create(
        model="gpt-5.6",
        input=PROMPT,
    )
    print(PROMPT)
    print(f"<Answer>\n{response.output_text}\n</Answer>")