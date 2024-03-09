from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.messages import get_buffer_string
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
import dotenv

dotenv.load_dotenv()

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

contextualize_template = (
    """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
)

contextualize_prompt = PromptTemplate.from_template(contextualize_template)


contextualize_chain = RunnableParallel(
    standalone_question=RunnablePassthrough.assign(
        chat_history=lambda x: get_buffer_string(x["history"])
    )
    | contextualize_prompt
    | llm
    | StrOutputParser(),
)
