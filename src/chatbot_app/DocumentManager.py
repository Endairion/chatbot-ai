import os
import shutil
import asyncio
import aiohttp
import aiofiles
from dotenv import load_dotenv
from llama_parse import LlamaParse
from langchain.schema.document import Document
from llama_index.core import SimpleDirectoryReader
from langchain_text_splitters import MarkdownHeaderTextSplitter
load_dotenv()


class DocumentManager:
    def __init__(self, new_path=None, old_path=None, db_path=None,):
        self.new_path = 'data/source/new'
        self.old_path = 'data/source/old'
        self.db_path = 'data/chroma'
        self.llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
        self.open_api_key = os.getenv("OPENAI_API_KEY")

    def parse_documents(self):
        if not os.listdir(self.new_path):
            print("No documents to be parsed.")
            return

        parser = LlamaParse(
            api_key=self.llama_cloud_api_key,
            result_type="markdown",
            gpt4o_mode=True,
            gpt4o_api_key=self.open_api_key,
            parsing_instructions="Do not parse any photos, images, logs, or screenshots. Only parse texts.",
            invalidate_cache=True,
            do_not_cache=True,
        )

        file_extractor = {".pdf": parser}
        documents = SimpleDirectoryReader(input_dir=self.new_path, file_extractor=file_extractor).load_data()

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

        if not os.path.exists(self.old_path):
            os.makedirs(self.old_path)

        files = os.listdir(self.new_path)
    
        for file_name in files:
            # Construct full file path
            full_file_name = os.path.join(self.new_path, file_name)
            
            if os.path.isfile(full_file_name):
                # Move the file
                shutil.move(full_file_name, self.old_path)

        return new_documents
    
    def split_documents(self, documents: list[Document]):
        print("Splitting documents into chunks.")
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, 
            return_each_line=False, 
            strip_headers=False)
        
        document = splitter.split_documents(documents)

        return document
    
    async def process_attachments(self, data):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for item in data:
                attachment_url = item.get('AttachmentPath')
                if attachment_url:
                    # Extract the filename from the URL
                    filename = os.path.basename(attachment_url)
                    
                    # Specify the path where the file will be saved
                    download_path = os.path.join(self.new_path, filename)  # Replace with your desired download path
                    
                    # Add a task to download the PDF asynchronously
                    tasks.append(self.download_pdf(session, attachment_url, download_path))
            
            # Wait for all download tasks to complete
            await asyncio.gather(*tasks)

    async def download_pdf(self, session: aiohttp.ClientSession, url, download_path):
        try:
            async with session.get(url) as response:
                response.raise_for_status()  # Raise an exception for HTTP errors
                
                # Save the PDF file
                async with aiofiles.open(download_path, 'wb') as f:
                    await f.write(await response.read())
                    print(f"Downloaded {os.path.basename(download_path)} successfully.")
        except aiohttp.ClientError as e:
            print(f"Error downloading {url}: {e}")
