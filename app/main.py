from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from fastapi import FastAPI 
from pydantic import BaseModel
from app.message_history_db.create_message_history_db import Conversations
from app.chains.contextualize_chain2 import contextualize_chain
from app.chains.rag_chain import qa_prompt, format_docs, _combine_documents
from app.retriever_chroma import build_retriever
from langchain.globals import set_verbose
from operator import itemgetter
from langchain.globals import set_debug

set_debug(True)
import dotenv

dotenv.load_dotenv()

factsbot = FastAPI()

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, verbose=True)

# Musimy skądś wziąc retrievera do naszego chroma db
retriever = build_retriever()

class chat_conversation(BaseModel):
    question: str
    session_id: int


@factsbot.post("/conversation")
async def conversation(data: chat_conversation):

    set_verbose(True)
    
    # Database holding message history
    history_instance = SQLChatMessageHistory(session_id=data.session_id, connection_string="sqlite:///message_history_db.db")

    # Wrapper for the contextualize chain, runnablewithmessagehistory manages message history for contextualize chain
    contextualize_chain_with_history = RunnableWithMessageHistory(
    contextualize_chain,
    lambda session_id: SQLChatMessageHistory(
        session_id=data.session_id, connection_string="sqlite:///message_history_db.db"
    ),
    input_messages_key="question",
    history_messages_key="history", 
    )

    # Running contextualize chain 
    contextualized_question = contextualize_chain_with_history.invoke(
        {"question": data.question},
        config={"configurable": {"session_id": data.session_id}}
    )


    rag_chain = {
        "context": itemgetter("standalone_question") | retriever | _combine_documents,
        "question": lambda x: x["standalone_question"],
    }


    # Final question
    answer_template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """

    ANSWER_PROMPT = ChatPromptTemplate.from_messages(
        [
            ("system", answer_template),
            ("human", "{question}"),
        ]
    )

    # Final chain
    conversational_qa_chain = contextualize_chain_with_history | rag_chain | ANSWER_PROMPT | llm | StrOutputParser()


    # Running final chain
    answer = conversational_qa_chain.invoke(
        {"question": data.question},
        config={"configurable": {"session_id": data.session_id}}
    )


    # Add question to the history
    if data.question:
        history_instance.add_user_message(message=data.question)

    # Add ai message to the history
    if answer:
        history_instance.add_ai_message(message=answer)
    

    return {"contextualized_question": contextualized_question, "rag_answer": answer}



    
