from openai import OpenAI
import numpy as np
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def get_embedding(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        input=texts, model="text-embedding-3-small"
    )
    return [item.embedding for item in response.data]


sentences = [
    "Fresh basil adds a fragrant, peppery note to homemade pasta sauce.",
    "Grilling vegetables brings out their natural sweetness and smoky flavor.",
    "A warm bowl of soup is the perfect comfort food on a cold day.",
    "Sushi combines vinegared rice with fresh fish, vegetables, or seafood.",
    "Baking bread from scratch fills the kitchen with a rich, yeasty aroma.",
    "A well-executed free throw requires balance, focus, and consistent form.",
    "Marathon runners often hit a mental wall around the twenty-mile mark.",
    "Soccer teams rely on quick passing to break through a tight defense.",
    "Swimmers shave seconds off their time by perfecting their turns.",
    "A strong serve can give a tennis player control of the entire match."
]

sentences_embeddings = [np.array(emb) for emb in get_embedding(sentences)]

def cosine_similarity(a, b):
  dot_prod = np.dot(a, b)
  norm_a = np.linalg.norm(a)
  norm_b = np.linalg.norm(b)
  return dot_prod / (norm_a * norm_b)

def search_similar(query: str):
    query_embedding = np.array(get_embedding([query])[0])
    similarities = [cosine_similarity(query_embedding, emb) for emb in sentences_embeddings]
    most_similar_index = np.argmax(similarities)
    return sentences[most_similar_index], similarities[most_similar_index]

print(search_similar("I am hungry."))