from collections import defaultdict
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain.schema.document import Document
import os
import json

markdown_file_path = os.path.abspath('D:/Projects/chatbot-ai/src/data/markdown/SKIM PENGILANGAN KONTRAK.md')
with open(markdown_file_path, 'r') as file:
    markdown_content = file.read()

headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on, 
    return_each_line=True, 
    strip_headers=False)
chunks = splitter.split_text(markdown_content)

print(chunks)

