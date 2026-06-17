import os
from dotenv import load_dotenv
from document_processor import process_document
from database import create_vector_db

load_dotenv()

if __name__ == "__main__":
    pdf_path = "documents/Cricket.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} is not present in the folder" )
    else:
        # Everything under here only happens if the file DOES exist!
        document_chunks = process_document(pdf_path)
        print(f"Success! We chopped the document into {len(document_chunks)} chunks.")

        if document_chunks:
            print("Building your vector database")
            db = create_vector_db(document_chunks)
            print("Database is ready!!!")


