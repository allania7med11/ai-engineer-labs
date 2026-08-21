import base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image, relative to this file
image_path = Path(__file__).parent / "files" / "receipt.png"

# Getting the Base64 string
base64_image = encode_image(image_path)

SYSTEM ='''You are a receipt image parser.
Your goal is to extract 4 pieces of information from it:
Total Amount: The final amount paid by the customer, equal to subtotal plus tax.
Date: The transaction date printed on the receipt, in YYYY-MM-DD format.
IS Healthy: true if most items are healthy (minimally processed, low added 
sugar/sodium/fat); false if most items are unhealthy/processed; null if 
undecidable.
Health Notes: 2-3 sentences explaining the decision based on the items.
Return them in JSON format, example:
{
    "total_amount": "$100",
    "date": "2026-08-17",
    "health_notes": "Most items are minimally processed, including bananas, chicken breast, Greek yogurt, and olive oil. There are only a couple of processed items like dish soap and paper towels, which aren't food. Overall, the grocery items lean healthy."
    "is_healthy": true,
}
'''
detail = "auto"
completion = client.chat.completions.create(
    model="gpt-5.6",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": SYSTEM},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": detail
                    },
                },
            ],
        }
    ],
)
print(f"detail: {detail}")
print(f"usage: {completion.usage}")
print(completion.choices[0].message.content)