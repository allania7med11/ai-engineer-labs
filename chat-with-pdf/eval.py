import json
from openai import OpenAI
from pyprojroot import here
from main import get_results
from tqdm import tqdm

data_path = here("chat-with-pdf/files/eval_set.json")

def found_in(fragment, strings):
    return any(fragment in s for s in strings)

def is_correct(gold, strings):
    for item in gold:
        alternatives = item if isinstance(item, list) else [item]
        if not any(found_in(alt, strings) for alt in alternatives):
            return False
    return True


if __name__ == "__main__":
    with open(data_path, "r") as f:
        data = json.load(f)

    client = OpenAI()
    score = 0
    answer = input("Eval with HyDE? (y/n): ").strip().lower()
    hyde = False
    if answer in ("y", "yes"):
        hyde = True

    for case in tqdm(data):
        query = case["q"]
        gold = case["gold"]
        results = get_results(query, hyde=hyde, client=client)
        strings = [r.page_content for r in results]
        if is_correct(gold, strings):
            score += 1
    print(f"Score: {score}/{len(data)}")