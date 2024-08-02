from dataclasses import dataclass
import gc
from chatbot_app.PromptTemplate import PromptTemplate
from chatbot_app.ChromaDB import ChromaDB
from chatbot_app.EmbeddingFunction import EmbeddingFunction
from chatbot_app.LanguageModel import LanguageModel

@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: list[str]

class RAGQuery:
    def __init__(self):
        self.db=None

    def __enter__(self):
        with EmbeddingFunction() as embedding_function:
            self.db = ChromaDB(embedding_function=embedding_function)
            self.db.setup_db()

        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.db
        gc.collect()

    def query(self, query_text: str) -> QueryResponse:
        if self.db is None:
            raise ValueError("DB not initialized. Call setup_db() first.")
        
        results = self.db.similarity_search(query_text, k=5)
        if len(results) == 0:
            print("Unable to find matching results.")
            return QueryResponse(
                query_text=query_text,
                response_text="Sorry, I couldn't find any relevant information.",
                sources=[]
            )
        
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        with PromptTemplate(question=query_text, context=context_text) as prompt:
            print(prompt)
            with LanguageModel(model_name="gpt-4o-mini", temperature=0.7) as model:
                response = model.generate(prompt)
                print(response)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        

        return QueryResponse(
            query_text=query_text,
            response_text=response,
            sources=sources
        )
    

