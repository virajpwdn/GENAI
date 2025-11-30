import warnings
# Suppress Pydantic V1 compatibility warning for Python 3.14
warnings.filterwarnings('ignore', category=UserWarning, module='langchain_core._api.deprecation')

from openai import OpenAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

client = OpenAI()

# Fixed: Added 'class' keyword
class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool
    
class ClassifyAccuracyResponse(BaseModel):
    response_accuracy: str

class State(TypedDict):
    query: str
    llm_result: str | None
    accuracy: str | None
    is_coding_question: bool | None

def classify_message(state: State):
    query = state['query']

    system_prompt = """
        You are an AI assistant. Your job is to detect if the user's query is related to coding question or not.
        Return the response in specified JSON boolean only.
    """
    
    # Fixed: Using correct API method and parameters
    response = client.beta.chat.completions.parse(
        model='gpt-4o-mini',  # Fixed: Using valid model name
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        response_format=ClassifyMessageResponse
    )

    is_coding_question = response.choices[0].message.parsed.is_coding_question
    print("THE VALUE OF IS CODING QUESTION - ", is_coding_question)
    
    # Fixed: Return updated state
    return {**state, "is_coding_question": is_coding_question}


def route_query(state: State) -> Literal["general_query", "coding_query"]:
    is_coding_question = state["is_coding_question"]
    
    if is_coding_question:
        return "coding_query"
    return "general_query"


def general_query(state: State):
    user_query = state['query']

    # Fixed: Removed extra brackets
    llm_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_query}
        ]
    )
    
    response = llm_response.choices[0].message.content
    
    return {**state, "llm_result": response}


def coding_query(state: State):
    user_query = state["query"]
    
    SYSTEM_PROMPT = """
        You are a coding expert and help user with coding. You explain them complex things with analogies and examples.
    """
    
    # Fixed: Removed extra brackets
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )
    
    return {**state, "llm_result": response.choices[0].message.content}


def coding_validate_query(state: State):
    llm_result = state["llm_result"]
    
    SYSTEM_PROMPT = f"""
        From the content which you receive, which will be related to coding, your task is to verify the content and give us accuracy.
        
        This is the content: {llm_result}
    """
    
    # Fixed: Using correct API method
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Analyze the accuracy of the above coding response."}
        ],
        response_format=ClassifyAccuracyResponse
    )
    
    accuracy = response.choices[0].message.parsed.response_accuracy
    
    return {**state, "accuracy": accuracy}


# Create a graph
graph_builder = StateGraph(State)

# Adding nodes to the graph
graph_builder.add_node("classify_message", classify_message)
graph_builder.add_node("general_query", general_query)
graph_builder.add_node("coding_query", coding_query)  # Fixed: Added missing node
graph_builder.add_node("coding_validate_query", coding_validate_query)

# Adding edges
graph_builder.add_edge(START, "classify_message")
graph_builder.add_conditional_edges("classify_message", route_query)

graph_builder.add_edge("general_query", END)
graph_builder.add_edge("coding_query", "coding_validate_query")
graph_builder.add_edge("coding_validate_query", END)

graph = graph_builder.compile()


def main():
    # Fixed: Correctly capture user input
    user_input = input("> ")
    
    _state: State = {
        "query": user_input,
        "accuracy": None,
        "is_coding_question": None,
        "llm_result": None
    }
    
    output = graph.invoke(_state)
    print("Output - ", output)


if __name__ == "__main__":
    main()