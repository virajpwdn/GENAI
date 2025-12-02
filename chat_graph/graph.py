# flake8: noqa
from typing_extensions import TypedDict
from typing import Annotated
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START,END
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
load_dotenv()

class State(TypedDict): 
    message: Annotated[list, add_messages]
    
llm = init_chat_model(model_provider="openai", model="gpt-4.1")

def chat_message(state: State):
    response = llm.invoke(state["message"])
    return {"message": [response]}

graph_builder = StateGraph(State)
graph_builder.add_node("chat_message", chat_message)
graph_builder.add_edge(START, "chat_message")
graph_builder.add_edge("chat_message", END)



def compile_graph_with_checkpointer(checkpoint):
    graph_with_checkpoint = graph_builder.compile(checkpointer=checkpoint)
    return graph_with_checkpoint

def main():
    DB_URI = "mongodb://root:example@mongo-db:27017"
    config = {"configurable": {"thread_id": "1"}}

    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        
        graph_with_mongo = compile_graph_with_checkpointer(mongo_checkpointer)
        
        query = input("> ")
        result = graph_with_mongo.invoke({"message": [{"role": "user", "content": query}]}, config=config)
        
        print("result", result)

main()