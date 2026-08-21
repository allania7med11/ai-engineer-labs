# receipt-parser

Photo of a receipt → total, date, and a healthy/unhealthy call with reasoning.

```
$ python main.py
<paste a real run here>
```

## Notes

- The image goes in as a base64 `data:` URL inside the message content, alongside the text part.
- `detail` controls how many tiles the image is cut into — it sets both cost and how much fine print survives.
- `usage` is printed so the token cost of an image is visible per run.

## Running

```bash
pip install openai python-dotenv
echo "OPENAI_API_KEY=sk-..." > .env
python main.py
```

Reads `files/receipt.png`.
