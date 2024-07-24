from langchain_community.vectorstores import Chroma
from langchain.schema.document import Document

class ChromaDB:
    def __init__(self,embedding_function):
        self.persist_directory = "data/chroma"
        self.embedding_function = embedding_function
        self.db = None
        
    def setup_db(self):
        self.db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding_function)

    def similarity_search(self, query_text: str, k: int):
        return self.db.similarity_search_with_score(query_text, k=k)
    
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
        

    def calculate_chunk_ids(self, documents: list[Document]):
        doc_chunk_counts = {}

        for doc_index, doc in enumerate(documents):
            filename = doc.metadata.get('filename', 'unknown_filename')
            header = doc.metadata.get('Header 1', 'no_header')

            # Create a unique document ID if it doesn't exist in the dictionary
            if filename not in doc_chunk_counts:
                doc_chunk_counts[filename] = {}
            
            # Create or update the header-specific chunk index within the document
            if header not in doc_chunk_counts[filename]:
                doc_chunk_counts[filename][header] = 0
            else:
                doc_chunk_counts[filename][header] += 1

            # Calculate the chunk ID using the filename, header, and header-specific chunk index
            chunk_id = f"{filename}:{header}:{doc_chunk_counts[filename][header]}"

            # Add the chunk ID to the document metadata
            doc.metadata["id"] = chunk_id
            print(chunk_id)

        return documents