import gc

PROMPT_TEMPLATE = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, politely say that you could not answer the question and tell the user to contact for customer support.
If you know the answer, just answer the question, don't make up an answer. 


Question: {question} 

Context: {context}
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