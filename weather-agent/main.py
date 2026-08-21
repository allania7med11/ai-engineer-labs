import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def get_weather(city: str) -> str:
    if city.capitalize() == "Tunis":
        return "Sunny"
    if city.capitalize() == "London":
        return "Rainy"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather information for a provided city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "A city for which to get weather information",
                    },
                },
                "required": ["city"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

messages = [{"role": "user", "content": "Should I wear a raincoat in New York?"}]

response = client.chat.completions.create(
    model="gpt-5.6",
    messages=messages,
    tools=tools,
    reasoning_effort="none"
)

messages.append(response.choices[0].message)

for tool_call in response.choices[0].message.tool_calls or []:
    if tool_call.function.name == "get_weather":
        args = json.loads(tool_call.function.arguments)
        weather = get_weather(args["city"])
        if weather:
            weather_info = {"weather": weather}
        else:
            weather_info = {"error": f"Weather information for {args['city']} is not available."}
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(weather_info),
            }
        )

response = client.chat.completions.create(
    model="gpt-5.6",
    messages=messages,
    tools=tools,
    reasoning_effort="none"
)

print(response.choices[0].message.content)