import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

def process_document(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
    )
    chunks = text_splitter.split_documents(pages)

    return chunks

if __name__ == "__main__":
    pdf_path = "documents/Cricket.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} is not present in the folder" )
    else:
        # Everything under here only happens if the file DOES exist!
        document_chunks = process_document(pdf_path)
        print(f"Success! We chopped the document into {len(document_chunks)} chunks.")

        if document_chunks:
            print("\nHere is a tiny piece of the very first chunk:")
            print("---------------------------------------------")
            print(document_chunks[0].page_content[:200] + "...")
            print("---------------------------------------------")
