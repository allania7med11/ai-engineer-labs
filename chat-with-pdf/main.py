import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""   # must run before any torch/docling import
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from langchain_docling import DoclingLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import hashlib

from openai import OpenAI
from pyprojroot import here
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.accelerator_options import AcceleratorOptions, AcceleratorDevice
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption

pdf_path = here("chat-with-pdf/files/embeddings & vector stores.pdf")

def get_loader(pdf_path):
    opts = PdfPipelineOptions()
    opts.do_ocr = False
    opts.accelerator_options = AcceleratorOptions(device=AcceleratorDevice.CPU, num_threads=os.cpu_count())

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
    )
    chunker = HybridChunker(tokenizer="sentence-transformers/all-MiniLM-L6-v2", max_tokens=256)

    loader = DoclingLoader(
        file_path=str(pdf_path),
        converter=converter,
        chunker=chunker,
    )
    return loader
    
loader = get_loader(pdf_path)
chunks = loader.load()   # list of LangChain Documents


def flatten_metadata(chunk):
    dl_meta = chunk.metadata.pop("dl_meta")
    chunk.metadata["page"] = dl_meta["doc_items"][0]["prov"][0]["page_no"]
    chunk.metadata["headings"] = " > ".join(dl_meta.get("headings", []))
    return chunk


chunks = [flatten_metadata(chunk) for chunk in chunks]

def chunk_id(chunk):
    key = f"{chunk.metadata['source']}|{chunk.metadata['page']}|{chunk.page_content}"
    return hashlib.sha256(key.encode()).hexdigest()


ids = [chunk_id(chunk) for chunk in chunks]

def get_vector_store():
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(
        collection_name="pdf_chunks",
        embedding_function=embeddings,
        persist_directory="chroma_langchain_db",
    )
    return vector_store

vector_store = get_vector_store()
vector_store.add_documents(documents=chunks, ids=ids)

def get_hyde(user_query, client=None):
    if client is None:
        client = OpenAI()
    hyde_prompt = f"Write a single paragraph, in the style of a technical whitepaper, that answers the question below. No headings, lists, or references.\n{user_query}"
    hyde_response = client.responses.create(
        model="gpt-5.6",
        input=hyde_prompt,
        max_output_tokens=300,
    )
    return hyde_response.output_text


def get_results(user_query, hyde=False, client=None):
    query = user_query
    if hyde:
        query = get_hyde(user_query, client=client)
    results = vector_store.similarity_search(
        query,
        k=5,
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

if __name__ == "__main__":
    while True:
        user_query = input("Enter your question (or 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break

        results = get_results(user_query, hyde=True, client=client)
        PROMPT = get_prompt(user_query, results)
        response = client.responses.create(
            model="gpt-5.6",
            input=PROMPT,
        )
        print(f"<Answer>\n{response.output_text}\n</Answer>")