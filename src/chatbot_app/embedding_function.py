from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_function():
    model_name = "intfloat/multilingual-e5-large"
    model_kwargs = {'device': 'cpu'}
    embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    )
    return embedding


if __name__ == "__main__":
    embedding = get_embedding_function()
    text = "Hello, how are you?"
    query = embedding.embed_query(text)
    print(query)
