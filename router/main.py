from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from IPython.display import Image, display

class State(TypedDict):
    user_input: str
    user_response: str

def solve_math_problem(state: State) -> str:
    # Placeholder for the actual math problem solving logic
    return {"user_response": "Math problem solved"}

def write_short_poem(state: State) -> str:
    # Placeholder for the actual poem writing logic
    return {"user_response": "Short poem written"}



def classifier(state: State) -> str:
    user_input = state['user_input'] 
    if "math" in user_input.lower():
        return "solve_math_problem"
    elif "poem" in user_input.lower():
        return "write_short_poem"
    return "get_user_response"

def get_user_response(state: State) -> str:
    # Placeholder for the actual poem writing logic
    if state['user_response']:
        print(state['user_response'])
    else:
        print("No response available")

builder = StateGraph(State)
builder.add_node("solve_math_problem", solve_math_problem)
builder.add_node("write_short_poem", write_short_poem)
builder.add_node("get_user_response", get_user_response)
builder.add_conditional_edges(START, classifier)
builder.add_edge("solve_math_problem", "get_user_response")
builder.add_edge("write_short_poem", "get_user_response")
builder.add_edge("get_user_response", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

if __name__ == "__main__":
    user_input = input("What do you need help with? ")
    graph.invoke({"user_input" : user_input})
