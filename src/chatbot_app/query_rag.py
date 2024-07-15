from dataclasses import dataclass
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
# from chatbot_app.embedding_function import get_embedding_function
from embedding_function import get_embedding_function
from dotenv import load_dotenv
import json
import os

CHROMA_PATH = "data/chroma" 

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]

def query_rag(query_text: str) -> QueryResponse:
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)
    if len(results) == 0:
        print("Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatOpenAI(model="ft:gpt-3.5-turbo-0125:personal::9hUiZayg", temperature=0)
    response = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    # Convert the AIMessage object to a JSON string
    response_text = response.content

    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return QueryResponse(
        query_text=query_text,
        response_text=response_text,
        sources=sources
    )

if __name__ == "__main__":
    query_text = ""
    query_rag(query_text)