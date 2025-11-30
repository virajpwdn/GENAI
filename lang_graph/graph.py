from langgraph.graph import StateGraph, START, END  
from typing_extensions import TypedDict
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

class State(TypedDict) :
    query: str
    llm_result: str | None


# The below function is simply a external tool
# Below chat bot is the node
def chat_bot(state: State) :
    # Extract Query From State
    user_query = state["query"]

    # Append LLm Result in state
    llm_result = client.chat.completions.create(model="gpt-4.1-nano", messages=[
        {"role": "user", "content": user_query}
    ])
    result = llm_result.choices[0].message.content

    state["llm_result"] = result

    return state

graph_builder = StateGraph(State)
graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)

graph = graph_builder.compile()

def main() :
    user = input("> ")

    _state = {
        "query": user,
        "llm_result": None
    }

    graph_result = graph.invoke(_state)
    print("Graph Results ", graph_result)

main()