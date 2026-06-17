from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain 
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

def setup_chatbot(vector_store):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    system_prompt = (
         "You are a helpful assistant. Use the provided context to answer the user's question. "
         "If you don't know the answer, just say that you don't know. Do not make things up.\n\n"
         "Context: {context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system",system_prompt),
        ("human","{input}"),
    ])
    retriever = vector_store.as_retriever()

    question_answer_chain = create_stuff_documents_chain(llm,prompt)
    rag_chain = create_retrieval_chain(retriever,question_answer_chain)

    return rag_chain
