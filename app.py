import streamlit as st
import os
from dotenv import load_dotenv
from document_processor import process_document
from database import create_vector_db
from chatbot import setup_chatbot

load_dotenv()

st.set_page_config(page_title="RAG Chatbot", page_icon = "icon.png", layout="centered")
st.title("RAG Chatbot")
st.caption("Upload a PDF and ask questions about it!")

if "chain" not in st.session_state:
    st.session_state.chain=None
if "messages" not in st.session_state:
    st.session_state.messages = []


# --- Sidebar: PDF Upload ---

with st.sidebar:
    st.header("Upload PDF")
    uploaded_pdf = st.file_uploader("Choose a PDF", type="pdf")
    if uploaded_pdf and st.session_state.chain is None:
        temp_path = f"temp_{uploaded_pdf.name}"
        with open(temp_path,"wb") as f:
                f.write(uploaded_pdf.getbuffer())
        
        with st.spinner("Reading and chunking the file"):
            chunks = process_document(temp_path)
            st.info(f'Created {len(chunks)} chunks!')
        
        with st.spinner("Building Vector database..."):
            db=create_vector_db(chunks)

        with st.spinner("Waking up the AI Assistant..."):
            st.session_state.chain = setup_chatbot(db)
        
        os.remove(temp_path)
        st.success("Ready! ask me anything.")

# --- Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your PDF..."):
    if st.session_state.chain is None:
        st.warning("Please upload a PDF first!")
    else:
        st.session_state.messages.append({"role":"user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chain.invoke({"input":prompt})
                answer = response["answer"]
            st.markdown(answer)
        st.session_state.messages.append({"role":"assistant","content":answer})




        
