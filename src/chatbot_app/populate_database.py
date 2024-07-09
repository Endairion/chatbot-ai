from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import Language
from chatbot_app.embedding_function import get_embedding_function
import argparse
import os 
import shutil
import re
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

load_dotenv()

DATA_PATH = 'data/source'# Path to the directory containing the PDF files.
DB_PATH = 'data/chroma'
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

def populate():
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

# Load the data
def load_documents():
    # parser = LlamaParse(
    #     api_key=LLAMA_CLOUD_API_KEY,
    #     result_type="markdown",
    # )
    
    # fileExtractor = {".pdf": parser}
    # documents = SimpleDirectoryReader(input_dir=DATA_PATH,file_extractor=fileExtractor).load_data()
    
    # print(f"Number of documents loaded: {len(documents)}")
    # print(documents)
    # output_dir = os.path.abspath("D:\Projects\chatbot-ai\src\data\markdown")
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)

    # for doc in documents:
    #     file_name = os.path.join(output_dir, f"{doc.id_}.md")
    #     with open(file_name, 'w') as f:
    #         f.write(doc.text)

    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    return documents

def split_documents(documents: list[Document]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=DB_PATH, 
        embedding_function=get_embedding_function()
    )

    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")


    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            # print(chunk)
            new_chunks.append(chunk)
            # print(new_chunks)

    if len(new_chunks):
        print(f"Adding {len(new_chunks)} new documents to the database.")
        new_chunks_ids = [chunk.metadata["id"] for chunk in new_chunks]
        print(new_chunks_ids)
        db.add_documents(documents=new_chunks, ids=new_chunks_ids)
    else:
        print("No new documents to add to the database.")

def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id
        print(chunk_id)

    return chunks

if __name__ == "__main__":
    populate()