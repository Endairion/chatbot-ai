from typing import Dict, Optional
from langchain_chroma import Chroma
from langchain.schema.document import Document

class ChromaDB:
    def __init__(self,embedding_function):
        self.persist_directory = "chroma"
        self.embedding_function = embedding_function
        self.db = None
        
    def setup_db(self):
        self.db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding_function)

    async def similarity_search(self, query_text: str, k: int, filter: Optional[Dict[str, str]] = None):
        return await self.db.asimilarity_search_with_score(query_text, k=k, filter=filter)
    
    def add(self, chunks: list[Document]):
        chunks_with_ids = self.calculate_chunk_ids(chunks)
        existing_items = self.db.get(include=[])
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
            # print(new_chunks_ids)
            self.db.add_documents(documents=new_chunks, ids=new_chunks_ids)
        else:
            print("No new documents to add to the database.")
        

    def calculate_chunk_ids(self,chunks):

        # This will create IDs like "data/monopoly.pdf:6:2"
        # Page Source : Page Number : Chunk Index

        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            current_page_id = f"{source}"
            current_chunk_index += 1

            # Calculate the chunk ID.
            chunk_id = f"{current_page_id}:{current_chunk_index}"

            # Add it to the page meta-data.
            chunk.metadata["id"] = chunk_id

        return chunks