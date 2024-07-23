import gc
from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingFunction:
    def __init__(self):
        self.embedding = None

    def __enter__(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name="intfloat/multilingual-e5-large", 
            model_kwargs={'device': "cpu"}
        )
        return self.embedding
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.embedding
        gc.collect()
        
        