from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4

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
uuids = [str(uuid4()) for _ in range(len(chunks))]
vector_store.add_documents(documents=chunks, ids=uuids)
results = vector_store.similarity_search(
    "Why is it acceptable for a search to return slightly wrong results if it runs much faster?",
    k=5,
)
for res in results:
    print(f"* {res.page_content} [{res.metadata}]")