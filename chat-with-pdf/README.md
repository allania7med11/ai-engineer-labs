# chat-with-pdf

Ask questions about a PDF and get answers grounded in its text, with the answer built only from the pages that were actually retrieved.

The document used here is Google's 50-page whitepaper *Embeddings & Vector Stores*.

```
$ python chat-with-pdf/main.py
Enter your question (or 'exit' to quit): What is ScaNN and how does it differ from HNSW?
<Answer>
ScaNN is Google's approximate nearest neighbour search approach ... HNSW instead uses a
multilayer proximity graph ...
</Answer>
```

## How it works

1. **Read the PDF.** Docling parses each page into headings, paragraphs, code blocks and tables, dropping headers and footers.
2. **Cut it into chunks.** Paragraphs are grouped under their section heading into pieces of at most 256 tokens. Each chunk remembers its page and heading.
3. **Store the chunks.** Every chunk is turned into an embedding and saved in a local Chroma database. Ids are content-based, so re-running never duplicates.
4. **Answer a question.** The question is embedded, the 5 closest chunks are pulled out, and the model is told to answer from those chunks only or say it doesn't know.

Optional step 4b, **HyDE**: before searching, the model writes a one-paragraph guess at the answer and that guess is used for the search instead of the raw question. The idea is that an answer looks more like a document chunk than a question does.

## Results

We wanted to know one thing: does HyDE find better chunks than searching with the plain question?

To answer it without guessing, we built a small test set: 30 questions about the paper, each labelled with the chunk or chunks a complete answer needs. Questions come in three flavours:

| kind | what it tests | count |
|---|---|---|
| verbatim | uses the paper's own words | 11 |
| paraphrase | same idea, everyday words | 12 |
| factoid | one specific number or name | 7 |

A question passes when every required chunk is among the 5 retrieved.

| search mode | questions passed | time for 30 questions |
|---|---|---|
| plain question | 27 / 30 | 9 seconds |
| HyDE | 29 / 30 | 3 min 53 s |

**What this means.** Plain search already answers 9 out of 10 questions on this document. HyDE picks up 2 more, but each question takes about 8 seconds instead of a fraction of a second, because a full model call runs before the search even starts. For a chat experience that is a long wait for a small gain.

**Decision.** Keep plain search as the default. HyDE stays in the code behind a flag for documents or users where wording differs a lot from the text.

**Caveats.** 30 questions on one clean document is a small test. The set was written by someone who had read the paper, so the questions are easier than real ones. With plain search already at 90 percent there is little room to show a difference either way. A harder test would use questions from people who haven't read the document, or fewer retrieved chunks.

## Running

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env

python chat-with-pdf/main.py    # chat with the PDF
python chat-with-pdf/eval.py    # run the 30-question test, choose HyDE on or off
```

Run from the repository root so the Chroma database lands in the same place each time. The first run parses the PDF and takes about a minute.

## Files

- `main.py` — parsing, chunking, storage, retrieval and the chat loop
- `eval.py` — scores retrieval against the test set
- `files/embeddings & vector stores.pdf` — the document
- `files/eval_set.json` — the 30 labelled questions
