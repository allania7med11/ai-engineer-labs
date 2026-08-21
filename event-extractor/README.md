# event-extractor

Conference PDF → validated JSON in one schema-constrained pass.

`files/sample-output.json` is a real run.

## Notes

- `response_format=AllEventDetails` — strict mode, so the shape is guaranteed, not requested.
- The root must be an object. `list[EventDetails]` is rejected outright; the list lives inside a wrapper.
- **The schema decides what you can extract.** A single-event schema returned 1 event out of 24 with
  no error and `finish_reason: "stop"` — the model discarded the rest to honour the shape.
- `reg_type` is an enum, so `paid` is unrepresentable unless listed. A missing enum value doesn't
  error, it comes back as a confident wrong label.
- `date` is `str`, so it drifts between runs (`Sep 25, 2026` / `September 25, 2026`). A `date` type
  would pin it. Known, not fixed.

## Running

```bash
pip install openai pydantic python-dotenv
echo "OPENAI_API_KEY=sk-..." > .env
# put your PDF at files/events.pdf
python main.py
```

Writes a timestamped file to `output/`.
