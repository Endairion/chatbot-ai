import gc

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context and the question's language: {question}
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