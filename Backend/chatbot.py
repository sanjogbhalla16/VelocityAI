#here we provide chatbot logic
from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain #This chain takes in chat history (a list of messages) and new questions, and then returns an answer to that question.
from langchain.memory import ConversationBufferMemory #A basic memory implementation that simply stores the conversation history.

llm = ChatOpenAI(model="gpt-4o",
    temperature=0.8,
    max_tokens=None,
    timeout=None,
    max_retries=2,)

memory = ConversationBufferMemory() #A basic memory implementation that simply stores the conversation history.
