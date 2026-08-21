
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field
from openai import OpenAI
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


class RegType(str, Enum):
    FREE = "free"
    EXTERNAL = "external"
    PAID = "paid"
    DONTKNOW = "dont_know"

class EventDetails(BaseModel):
    name: str
    date: str = Field(description="Event date, e.g. Sep 25, 2026")
    location: str = Field(description="Event location, e.g.  Agrigento, IT")
    reg_type : RegType= Field(description="Event registration type, e.g. free, external, paid, dont_know")
    topics: list[str]

class AllEventDetails(BaseModel):
    events: list[EventDetails]


ROOT = Path(__file__).parent
PDF = ROOT / "files" / "events.pdf"

file = client.files.create(file=open(PDF, "rb"), purpose="user_data")
completion = client.chat.completions.parse(
    model="gpt-5.6",
    messages=[
        {"role": "user", "content": [
            {
                    "type": "file",
                    "file": {
                        "file_id": file.id,
                    },
                },
            {"type": "text", "text": "Extract the event details."}
        ]},
    ],
    response_format=AllEventDetails,
)
event = completion.choices[0].message.parsed
ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
with open(f"{ROOT}/output/data_{ts}.json", "w") as f:
    f.write(event.model_dump_json(indent=2))