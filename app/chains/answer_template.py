from langchain_core.prompts import ChatPromptTemplate

# Define answer template
answer_template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

# Create ChatPromptTemplate for answer prompt
answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", answer_template),
        ("human", "{question}"),
    ]
)