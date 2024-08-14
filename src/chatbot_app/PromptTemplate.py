import gc

PROMPT_TEMPLATE ="""You are an expert assistant specialized in providing detailed and accurate information based on retrieved documents. Below is the context retrieved from the relevant documents, followed by the user's question. Please provide a detailed and accurate answer.

Context:
{context}

Question:
{question}

Instructions for the Answer:
- Provide a clear and concise answer.
- Only answer the question using the context, don't make up an answer.
- If you don't know the answer, politely say that you could not answer the question and tell the user to contact customer support.
- No mentioning "According to the context above", "Based on the context above", etc.
Answer:
"""


class PromptTemplate:
    def __init__(self, question: str, context: str):
        self.template = PROMPT_TEMPLATE
        self.question = question
        self.context = context

    def __enter__(self):
        return self.template.format(context=self.context, question=self.question)

    def __exit__(self, exc_type, exc_value, traceback):
        gc.collect()