from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from fastapi import FastAPI 
from pydantic import BaseModel
from app.chains.contextualize_chain import contextualize_chain
from app.chains.rag_chain import qa_prompt, format_docs, combine_documents, rag_chain
from app.chains.answer_template import answer_prompt
from langchain.globals import set_verbose
from langchain.globals import set_debug
import dotenv


# Load environment variables from .env file
dotenv.load_dotenv()

# Enable debug mode
set_debug(True)

# Create FastAPI app instance
app = FastAPI()

# Initialize ChatOpenAI instance
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, verbose=True)


# Define Pydantic model for chat conversation
class ChatConversation(BaseModel):
    question: str
    session_id: int


@app.post("/conversation")
async def conversation(data: ChatConversation):

    # Enable verbose mode
    set_verbose(True)
    
    # Database holding message history
    history_instance = SQLChatMessageHistory(session_id=data.session_id, connection_string="sqlite:///app/message_history_db/message_history_db.db")

    # Wrapper for the contextualize chain, runnablewithmessagehistory manages message history for contextualize chain
    contextualize_chain_with_history = RunnableWithMessageHistory(
    contextualize_chain,
    lambda session_id: history_instance,
    input_messages_key="question",
    history_messages_key="history", 
    )

    # Running contextualize chain 
    contextualized_question = contextualize_chain_with_history.invoke(
        {"question": data.question},
        config={"configurable": {"session_id": data.session_id}}
    )

    # Define conversational QA chain
    conversational_qa_chain = contextualize_chain_with_history | rag_chain | answer_prompt | llm | StrOutputParser()

    # Running conversational QA chain
    answer = conversational_qa_chain.invoke(
        {"question": data.question},
        config={"configurable": {"session_id": data.session_id}}
    )

    # Add question and answer to the history
    if data.question and answer:
        history_instance.add_user_message(message=data.question)
        history_instance.add_ai_message(message=answer)
    else:
        pass
        # Wypisanie bledu
    

    return {"contextualized_question": contextualized_question, "rag_answer": answer}



    
