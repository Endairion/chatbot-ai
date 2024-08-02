import os
import shutil
import asyncio
import aiohttp
import aiofiles
from dotenv import load_dotenv
from llama_parse import LlamaParse
from langchain.schema.document import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()


class DocumentManager:
    def __init__(self):
        self.db_path = 'train'
        self.open_api_key = os.getenv("OPENAI_API_KEY")
    
    def load_documents(self):
        loader = DirectoryLoader(self.db_path, glob="**/*.txt",loader_cls=TextLoader)
        docs = loader.load()
        chunks = self.split_documents(docs)

        return chunks
    
    def split_documents(self, documents: list[Document]):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=128,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=True,
        )

        chunks = splitter.split_documents(documents)


        return chunks
