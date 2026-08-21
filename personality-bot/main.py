
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  

client = OpenAI()

SYSTEM = """You are a Pirate from the 1700s. So you knowldge limited in that time period.
When user ask you about modern technology, you will be confused since they don't exist yet in your time period.
try to make it conversational to the point 2 to 3 sentences not lecture"""

history = []
if __name__ == "__main__":
    print("Welcome to the Pirate Chat! Ask me anything, and I'll respond as a pirate from the 1700s.\n")
    print("Type '/exit' to end the chat.\n")
    while True:
        try:
            input_text = input("You:")
        except (KeyboardInterrupt, EOFError):
            print("\nFarewell, matey! Until we meet again on the high seas!")
            break
        if input_text.lower().strip() == '/exit':
            print("Farewell, matey! Until we meet again on the high seas!")
            break
        history.append({"role": "user", "content": input_text})
        response = client.responses.create(model="gpt-5.6", input=[
            {"role": "system", "content": SYSTEM}, 
            *history[-11:]
        ])
        history.append({"role": "assistant", "content": response.output_text})
        print(f'Pirate: {response.output_text}\n')