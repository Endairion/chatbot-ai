import gc
from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingFunction:
    def __init__(self):
        self.embedding = None

    def __enter__(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name="Alibaba-NLP/gte-base-en-v1.5", 
            model_kwargs={'device': "cpu", 'trust_remote_code': True}
        )
        return self.embedding
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.embedding
        gc.collect()
        
        