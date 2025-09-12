from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path = Path(__file__).parent / "k8.pdf"

#loading
loder = PyPDFLoader(file_path=pdf_path)
docs = loder.load() # Read PDF File

# print("DOCS[0]", docs[5])


# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=50
)

# in docs we have the text which came from pdf, then text splitter is imported from langchain although we can create this splitter logic but langchain has already done this and it saves time. 

split_docs = text_splitter.split_documents(documents=docs)  # Here we are actually splliting the docs
# print("SPLITTED DOCS", split_docs)

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# using embedding_model create embedding of split_docs and store them in vector db

vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    url='http://localhost:6333',
    collection_name="learning_vectors",
    embedding=embedding_model
)

print("Indexing of Documents Done...")