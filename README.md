# ai-engineer-labs

Small, focused LLM systems built to production habits — structured outputs,
tool use, retrieval, agents. Each folder is standalone and runnable.

| Project | What it does | Key idea |
|---|---|---|
| personality-bot | CLI chat with a persona | roles, temperature, history |
| receipt-parser | photo → total + date | vision, cost per image |
| event-extractor | PDF → validated JSON | strict schema, enums |
| weather-agent | answers using a live tool | the tool-call loop |

## Stack
Python 3.12, OpenAI SDK, pydantic

## Running
`cp .env.example .env`, add your key, then see each project's README.
