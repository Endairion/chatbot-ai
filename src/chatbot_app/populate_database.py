import glob
from langchain_community.document_loaders import UnstructuredMarkdownLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import Language, MarkdownHeaderTextSplitter
from chatbot_app.embedding_function import get_embedding_function
# from embedding_function import get_embedding_function
import argparse
import os 
import shutil
import re
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

load_dotenv()

NEW_DATA_PATH = 'data/source/new'
OLD_DATA_PATH = 'data/source/old'
DB_PATH = 'data/chroma'
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

def populate():
    document = parse_documents()
    chunks = split_documents(document)
    print(chunks)
    add_to_chroma(chunks)

# Load the data
def parse_documents():
    # Check if the NEW_DATA_PATH directory is empty
    if not os.listdir(NEW_DATA_PATH):
        print("No documents to be parsed.")
        return

    parser = LlamaParse(
        api_key=LLAMA_CLOUD_API_KEY,
        result_type="markdown",
        gpt4o_mode=True,
        gpt4o_api_key=OPEN_API_KEY,
        parsing_instructions="Do not parse any photos, images, logs, or screenshots. Only parse texts.",
        invalidate_cache=True,
        do_not_cache=True,
    )
    
    fileExtractor = {".pdf": parser}
    documents = SimpleDirectoryReader(input_dir=NEW_DATA_PATH,file_extractor=fileExtractor).load_data()
    
    # Iterate through the documents and concatenate their content
    new_documents = []
    filename = None
    content = None

    for document in documents:
        if filename is None:
            filename = document.metadata["file_name"]
            content = document.text
        elif filename == document.metadata["file_name"]:
            content += "\n" + document.text
        else:
            new_documents.append(Document(page_content=content, metadata={"filename": filename}))
            filename = None
            
    new_documents.append(Document(page_content=content, metadata={"filename": filename}))

    # Ensure the OLD_DATA_PATH directory exists
    if not os.path.exists(OLD_DATA_PATH):
        os.makedirs(OLD_DATA_PATH)

    # List all files in the NEW_DATA_PATH directory
    for filename in os.listdir(NEW_DATA_PATH):
        new_file_path = os.path.join(NEW_DATA_PATH, filename)
        old_file_path = os.path.join(OLD_DATA_PATH, filename)

        # Move each file to the OLD_DATA_PATH directory
        shutil.move(new_file_path, old_file_path)
        print(f"Moved {filename} to {OLD_DATA_PATH}")

    return new_documents

def split_documents(documents: list[Document]):
    print("Splitting documents into chunks.")
    headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, 
        return_each_line=False, 
        strip_headers=False)
    
    document= splitter.split_documents(documents)

    return document

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

def calculate_chunk_ids(documents: list[Document]):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index
    last_page_id = None
    current_chunk_index = 0
    for doc in documents:
        filename = doc.metadata.get('filename', 'unknown_filename')
        header = doc.metadata.get('Header 1', 'no_header')
        current_page_id = f"{filename}:{header}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        doc.metadata["id"] = chunk_id
        print(chunk_id)

    return documents



if __name__ == "__main__":
    populate()