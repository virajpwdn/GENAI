from openai import OpenAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def ClassifyMessageResponse(BaseModel):
    is_coding_question: bool

class State(TypedDict):
    query: str
    llm_result: str | None
    accuracy: str | int
    is_coding_question: bool | None


def classify_message(state: State):
    # Structured Outputs / Response

    query = state['query']

    system_prompt = """
        You are an AI assistant. Your job is to detect if the user's query is related to coding question or not.
        Return the response in specifies JSON boolean only.
    """
    response = client.responses.parse( 
        model='gpt-4.1-nano',
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        text_format=classify_message
    )

    is_coding_question = response.output_parsed
    print("THE VALUE OF IS CODING QUESTION - ", is_coding_question)
    state["is_coding_question"] = is_coding_question

