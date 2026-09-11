from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from IPython.display import Image, display
from openai import OpenAI
from pydantic import BaseModel
from typing import Literal
from textwrap import dedent

class UserQuery(BaseModel):
    type: Literal["math", "poem", "other"]

client = OpenAI()

class State(TypedDict):
    user_input: str
    query_type: str
    user_response: str

def solve_math_problem(state: State) -> str:
    PROMPT = dedent(f"""\
        You are a helpful assistant that solves math problems.
        You will receive a user query that contains a math problem, and you must provide the solution
        <USER QUERY>
        {state['user_input']}
        </USER QUERY>       
    """)
    response = client.responses.create(
        model="gpt-6-astra",
        input=PROMPT,
    )
    return {"user_response": response.output_text}

def write_short_poem(state: State) -> str:
    PROMPT = dedent(f"""\
        You are a helpful assistant that writes short poems.
        You will receive a user query that contains a request for a poem, and you must provide the poem
        <USER QUERY>
        {state['user_input']}
        </USER QUERY>       
    """)
    response = client.responses.create(
        model="gpt-6-astra",
        input=PROMPT,
    )
    return {"user_response": response.output_text}



def classifier(state: State) -> str:
    SYSTEM = dedent("""\
        You are a helpful assistant that classifies user queries into one of three categories: 
        math, poem, or other. 
        You will receive a user query and must determine its type based on the content. 
        If the query is related to mathematics, classify it as 'math'. 
        If it is a request for a poem, classify it as 'poem'. 
        For all other queries, classify them as 'other'
    """)
    user_input = state['user_input'] 
    completion = client.chat.completions.parse(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": user_input,
            },
        ],
        response_format=UserQuery,
    )
    query: UserQuery = completion.choices[0].message.parsed
    return {"query_type": query.type}

def decide_node(state: State) -> str:
    query_type = state['query_type']
    if query_type == "math":
        return "solve_math_problem"
    elif query_type == "poem":
        return "write_short_poem"
    else:
        return "get_user_response"

def get_user_response(state: State) -> str:
    # Placeholder for the actual poem writing logic
    if 'user_response' in  state:
        print(state['user_response'])
    else:
        print("No response available")

builder = StateGraph(State)
builder.add_node("classifier", classifier)
builder.add_node("solve_math_problem", solve_math_problem)
builder.add_node("write_short_poem", write_short_poem)
builder.add_node("get_user_response", get_user_response)
builder.add_edge(START, "classifier")
builder.add_conditional_edges("classifier", decide_node)
builder.add_edge("solve_math_problem", "get_user_response")
builder.add_edge("write_short_poem", "get_user_response")
builder.add_edge("get_user_response", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

if __name__ == "__main__":
    user_input = input("What do you need help with? ")
    graph.invoke({"user_input" : user_input})
