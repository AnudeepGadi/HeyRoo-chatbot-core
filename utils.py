from langchain_community.document_loaders.s3_file import S3FileLoader
from typing import List, ByteString
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import pickle
from chromadb import Collection
from langchain_community.vectorstores import Chroma
import time

endpoint = 'http://127.0.0.1:9000'
access_key = 'UZ3l8yV6SohDj3Jlisfp'
secret_key = '6Y8XEJcCUwIARDBPtN9u2GG84iuuH08rOKRVeF7n'
use_ssl = False
file_u = "umkc-student-handbook.pdf"

embeddings = HuggingFaceEmbeddings( model_name="thenlper/gte-large",
   encode_kwargs={"normalize_embeddings": True}
   )

def print_time():
    current_time = time.localtime()
    formatted_time = time.strftime("%H:%M:%S.%m", current_time)
    print(formatted_time)

def load_document_from_s3(bucket:str, key:str)->List[Document]:
    file_loader = S3FileLoader(
        bucket=bucket,
        key=key,
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        use_ssl=use_ssl
    )
    document = file_loader.load()
    return document

def create_chunks(documents: List[Document]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    return chunks

def document_to_binary(doc:Document):
    return pickle.dumps(doc)

def binary_to_document(binary_data: ByteString):
    return pickle.loads(binary_data)

    
def save_to_vector_store(collection:Collection,chunk:Document):
    embedding = embeddings.embed_query(chunk.page_content)
    collection.add(
        documents=[chunk.page_content],
        metadatas=[chunk.metadata],
        embeddings= embedding,
        ids=[str(collection.count()+1)]
    )

def delete_embeddings(path:str):
    col
