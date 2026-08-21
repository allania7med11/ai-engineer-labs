# personality-bot

CLI chat bot that stays in character as a 1700s pirate and gets confused by modern technology.

```
$ python main.py
You: <paste a real exchange here>
```

## Notes

- `SYSTEM` is prepended to every request — the model keeps nothing between calls.
- `history` is a list you own and resend in full.
- `history[-11:]` bounds it: unbounded, the payload grows every turn and you pay for all of it.

## Running

```bash
pip install openai python-dotenv
echo "OPENAI_API_KEY=sk-..." > .env
python main.py
```

`/exit` to quit.
