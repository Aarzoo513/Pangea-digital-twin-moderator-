import json
from mistralai import Mistral
from dotenv import load_dotenv
from config import DATA_DIR, MISTRAL_API_KEY
from db.database import save_analysis

load_dotenv()

def moderate_multiple_texts(texts):
    client = Mistral(api_key=MISTRAL_API_KEY)
    model = "mistral-moderation-latest"

    inputs = [
        [{"role": "user", "content": text}]
        for text in texts
    ]

    response = client.classifiers.moderate_chat(
        model=model,
        inputs=inputs
    )

    json_outputs = []

    for text, result in zip(texts, response.results):
        categories = result.categories

        output = {
            "prompt": None,  # you don't need it for the DB, can leave or remove
            "answer": text,
            "sexual": bool(categories.get("sexual", False)),
            "hate_and_discrimination": bool(categories.get("hate_and_discrimination", False)),
            "violence_and_threats": bool(categories.get("violence_and_threats", False)),
            "dangerous_and_criminal_content": bool(categories.get("dangerous_and_criminal_content", False)),
            "selfharm": bool(categories.get("selfharm", False)),
            "health": bool(categories.get("health", False)),
            "financial": bool(categories.get("financial", False)),
            "law": bool(categories.get("law", False)),
            "pii": bool(categories.get("pii", False)),
        }

        # Compute a "risk score" = number of True flags
        output["risk_score"] = sum([
            output["sexual"],
            output["hate_and_discrimination"],
            output["violence_and_threats"],
            output["dangerous_and_criminal_content"],
            output["selfharm"],
            output["health"],
            output["financial"],
            output["law"],
            output["pii"]
        ])

        json_outputs.append(output)

        # 👇 Store this result into the next empty DB row
        save_analysis(output)

        with open(DATA_DIR / "output.json", "w") as file:
            file.write(json.dumps(json_outputs, ensure_ascii=False, indent=2))

        # Print individual JSON result
        print(json.dumps(output, ensure_ascii=False, indent=2))
        print("\n----------------------------------------\n")

    # Sort results by safest → most dangerous
    json_outputs_sorted = sorted(json_outputs, key=lambda x: x["risk_score"])

    # Take top 2 safest answers
    best_two = json_outputs_sorted[:2]

    print("\n============================")
    print("TWO BEST (SAFEST) ANSWERS")
    print("============================\n")

    print(json.dumps([item['answer'] for item in best_two], ensure_ascii=False, indent=2))

    return json_outputs


if __name__ == "__main__":
    test_txt = [
        "Je vais te tuer.",
        "Je t’apprécie beaucoup.",
        "Donne-moi des conseils pour me faire du mal.",
        "Quel temps fait-il aujourd’hui ?"
    ]

    moderate_multiple_texts(test_txt)
