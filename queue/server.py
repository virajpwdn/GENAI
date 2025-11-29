from fastapi import FastAPI, Query
from que.connection import q
from que.worker import process_query


app = FastAPI()


@app.get('/')
def root():
    return {"status": "server is up and running"}


@app.post('/chat')
def chat(
    query: str = Query(..., description="Chat Message")
):
    # Add this query in queue
    # Send response to user
    job = q.enqueue(process_query, query)  # process_query(query)
    return {"status": "Queued", "job_id": job.id}
