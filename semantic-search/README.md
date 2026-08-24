# semantic-search

Ranks 10 sentences (5 food, 5 sports) against a query by meaning, not keywords.

```
$ python main.py
('A warm bowl of soup is the perfect comfort food on a cold day.', 0.2667525502419823)
```

`"I am hungry."` shares no word with any sentence. Keyword search returns nothing.

## Notes

- **The whole list is one API call.** `input=` takes a list — 10 sentences, one round trip.
  Calling per sentence is 10× the latency for the same cost.
- **`0.27` is the top match, and that's fine.** Absolute cosine scores are meaningless on their own;
  the floor is a property of the model, not a constant (~0.7 for `ada-002`, far lower for
  `-3-small`). Rank the results — don't threshold on a number you picked by eye.
- **Cosine strips magnitude.** The dot product sums per-axis agreement; dividing by both lengths
  leaves only orientation, so a long sentence and a short one are comparable.
- **A numpy array *is* a vector store** at this size. Chroma/FAISS add persistence, metadata
  filtering, and ANN indexes that skip most of the corpus — none of which 10 rows need.
- **Vectors are model-specific.** Switching embedding models means re-embedding everything;
  a cosine between two models is noise.

## Running

```bash
pip install openai numpy python-dotenv
echo "OPENAI_API_KEY=sk-..." > .env
python main.py
```
