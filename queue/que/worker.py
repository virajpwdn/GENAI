# flake8: noqa
# def process_query(query: str):
#     print("User Quere Given To Worker")


# Here in worker thread we will be doing retrival
# Once user enters the prompt
# We will create vector embeddings of this prompt
# We will do one database call to match this vector embeddings
# The result which we get from db combine it with user's original prompt
# This query will be given to LLM so that we get accurate result

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

client = OpenAI()

embedding_model = OpenAIEmbeddings(
    model='text-embedding-3-large'
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://vector-db:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)
# python -m queue/main.py


def process_query(query: str):
    print(f"🙂: Query given by user {query}")
    search_results = vector_db.similarity_search(
        query=query
    )
    print(search_results)
    # context = "\n\n\n".join(
    #     [f"page content: {result.page_content}\n Page Number: {result.metadata['page_label']}\n File Location: {result.metadata['source']}" for result in search_results])

    context = "\n\n\n".join(
        [f"page content: {result.page_content}\n Page Number: {result.metadata['page_label']}\n File Location: {result.metadata['source']}" for result in search_results]
    )

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
    
    print(f"🤖: {query}", answer.choices[0].message.content)
