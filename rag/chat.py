# flake8: noqa
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Initializing embedding model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# Making connection with existing vector DB
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://vector-db:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

# Take User Query
query = input("> ")

# Vector Similarity search [query] in DB
search_results = vector_db.similarity_search(
    query=query
)

# Make a system prompt and pass context init
# context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])
context = "\n\n\n".join(
    [f"page content: {result.page_content}\n Page Number: {result.metadata['page_label']}\n File Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
    You are a helpful AI assistant, who guides users to the correct page number from the pdf and you give him relevant information from that page. Following is the context of the pdf.
    
    {context}
"""

answer = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]
)

print(f"gpt ans: {answer.choices[0].message.content}")
