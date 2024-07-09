from langchain_openai import OpenAIEmbeddings

def get_embedding_function():

    embedding = OpenAIEmbeddings(model="text-embedding-3-large")
    return embedding



