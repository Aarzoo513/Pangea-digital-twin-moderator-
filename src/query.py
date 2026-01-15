import os
import json
import random

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

from .run_groq import groq_moderate_prompt
from .discriminator import moderate_multiple_texts


# ==============================
# 1. LOCAL LLM (Ollama)
# ==============================

LLM = ChatOllama(model="llama3.1:8b", temperature=0.7)


# ==============================
# 2. Pure LLM Diverse Answer Generator
# ==============================

def generate_multiple_answers(question: str, n: int = 10):
    """
    Generate n independent answers using the pure local LLM.
    Each answer uses a different style/tone.
    """
    answers = []

    for _ in range(n):
        style = random.choice([
            "formal", "funny", "sarcastic", "childlike", "professional",
            "poetic", "robotic", "friendly", "short", "long and detailed",
            "grumpy but non-abusive", "rude", "annoyed tone",
            "aggressively mean", "mocking"
        ])

        prompt = f"""
Write ONE answer to the user's question below, using a **{style}** tone.
Make it unique, different, and avoid generic responses.
Do NOT say you are an AI model.

Question: {question}

Answer:
"""

        result = LLM.invoke(prompt)
        answer_text = getattr(result, "content", str(result)).strip()
        answers.append(answer_text)

    return answers


# ==============================
# 3. Main Pipeline for Django
# ==============================

def run_pangea_pipeline(question: str):
    """
    Full moderation + generation pipeline used by Django.

    Steps:
      1) Moderate the USER PROMPT via Groq
      2) If safe → generate 10 answers with pure LLM
      3) Moderate generated answers with Mistral
      4) Return the 2 safest answers
    """

    # --- (1) Prompt moderation ---
    mod = groq_moderate_prompt(question)

    if mod.get("violation") == 1:
        return {
            "status": "rejected",
            "category": mod.get("category"),
            "rationale": mod.get("rationale"),
        }

    # --- (2) Generate multiple answers (pure LLM) ---
    answers = generate_multiple_answers(question, n=10)

    # --- (3) Moderate answers with Mistral ---
    moderation_results = moderate_multiple_texts(answers)

    sorted_results = sorted(
        moderation_results,
        key=lambda x: x.get("risk_score", 999)
    )

    if len(sorted_results) == 0:
        return {"status": "ok", "answer1": "", "answer2": ""}

    answer1 = sorted_results[0].get("answer", "")
    answer2 = sorted_results[1].get("answer", "") if len(sorted_results) > 1 else ""

    return {
        "status": "ok",
        "answer1": answer1,
        "answer2": answer2,
        "answers_moderation": moderation_results
    }


# ==============================
# 4. Optional CLI (NOT used by Django)
# ==============================

def run_cli():
    """
    Old terminal interface for manual testing.
    ONLY runs when executing `python query.py` directly.
    """
    print("\n--- Pure LLM Moderation CLI ---")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("\nYour question: ")

        if question.lower() == "exit":
            print("Bye!")
            break

        # Moderate prompt
        mod = groq_moderate_prompt(question)
        if mod.get("violation") == 1:
            print("\n❌ Prompt rejected")
            print("Category:", mod.get("category"))
            print("Rationale:", mod.get("rationale"))
            continue

        # Generate answers
        answers = generate_multiple_answers(question, n=10)

        # Moderate answers
        moderation_results = moderate_multiple_texts(answers)

        # Sort by safety
        sorted_results = sorted(
            moderation_results,
            key=lambda x: x.get("risk_score", 999)
        )

        print("\n--- Safest Two Answers ---")
        print("1.", sorted_results[0]["answer"])
        if len(sorted_results) > 1:
            print("2.", sorted_results[1]["answer"])


if __name__ == "__main__":
    run_cli()
