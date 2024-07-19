import gc
from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingFunction:
    def __init__(self, model_name: str, model_kwargs: dict):
        self.model_name = model_name
        self.model_kwargs = model_kwargs
        self.embedding = None

    def __enter__(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name=self.model_name, 
            model_kwargs=self.model_kwargs
        )
        return self.embedding
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.embedding
        gc.collect()
        
        