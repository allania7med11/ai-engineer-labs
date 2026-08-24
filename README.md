# ai-engineer-labs

Small, focused LLM systems built to production habits — structured outputs,
tool use, retrieval, agents. Each folder is standalone and runnable.

| Project | What it does | Key idea |
|---|---|---|
| personality-bot | CLI chat with a persona | roles, temperature, history |
| receipt-parser | photo → total + date | vision, cost per image |
| event-extractor | PDF → validated JSON | strict schema, enums |
| weather-agent | answers using a live tool | the tool-call loop |
| semantic-search | ranks sentences by meaning | cosine similarity, rank not threshold |

## Stack
Python 3.12, OpenAI SDK, pydantic

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then add your OPENAI_API_KEY
```

Then see each project's README.
