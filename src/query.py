from langchain_huggingface import HuggingFaceEmbeddings  # <-- LOCAL Embeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama               # <-- LOCAL LLM
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from .run_groq import groq_moderate_prompt
import random
import json
import os

# Path to Pangea folder
"""PANGEA_PATH = os.path.join(
    os.path.dirname(__file__),
    "Pangea-digital-twin-moderator-"
)

sys.path.append(PANGEA_PATH)"""

from .discriminator import moderate_multiple_texts

# --- 1. Configuration ---
VECTOR_STORE_PATH = "./chroma_db"
EMBEDDINGS_MODEL = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
LLM = ChatOllama(model="llama3.1:8b", temperature=0.7)

if not os.path.exists(VECTOR_STORE_PATH):
    print(f"Error: Vector store not found at {VECTOR_STORE_PATH}")
    print("Please run main.py first to create the database.")
    exit()

# --- 2. Connect to the Existing Local Database ---
print(f"Connecting to existing vector store at: {VECTOR_STORE_PATH}...")
docsearch = Chroma(
    persist_directory=VECTOR_STORE_PATH,
    embedding_function=EMBEDDINGS_MODEL  # Use the same embedder
)
print("Connected.")

# Define the Multi-Proposal Prompt
multi_proposal_template = """
Using the retrieved documents, produce 10 possible answers to the question.

Context: {context}
Question: {question}

Answer 1:
Answer 2:
Answer 3:
Answer 4:
Answer 5:
Answer 6:
Answer 7:
Answer 8:
Answer 9:
Answer 10:
"""
PROMPT = PromptTemplate(
    template=multi_proposal_template,
    input_variables=["context", "question"]
)

# making a different prompt for the pure llm
general_chat_template = """
Provide 10 different possible answers to the user's message.

User input: {question}

Answer 1:
Answer 2:
Answer 3:
Answer 4:
Answer 5:
Answer 6:
Answer 7:
Answer 8:
Answer 9:
Answer 10:
"""
GENERAL_CHAT_PROMPT = PromptTemplate(
    template=general_chat_template,
    input_variables=["question"]
)


def generate_multiple_answers(llm, question, n=10):
    answers = []

    for i in range(n):
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

        response = llm.invoke(prompt)

        # Extract the text cleanly
        answer_text = response.content.strip()

        answers.append(answer_text)

    return answers


# --- 3. Build the RAG Chain ---
print("Building RAG chain with Ollama...")
qa_chain = RetrievalQA.from_chain_type(
    llm=LLM,
    chain_type="stuff",
    retriever=docsearch.as_retriever(),
    chain_type_kwargs={"prompt": PROMPT},
    return_source_documents=False,
    input_key="question"
)
print("\n--- RAG (100% Local) is Ready ---")

pure_llm = ChatOllama(model="llama3.1:8b", temperature=0.7)

print("\n--- RAG (Hybrid Mode) is Ready ---")
print("Type '/toggle' to switch between RAG and General Chat.")
print("Type 'exit' to quit.\n")

rag_mode_on = True

# the general chain
general_chain = GENERAL_CHAT_PROMPT | pure_llm

all_generated_answers = []
# --- 4. Start the Question Loop ---
while True:
    # Visual cue for the user
    mode_label = "[ RAG]" if rag_mode_on else "[💬 GENERAL CHAT]"
    query = input(f"\n{mode_label} Enter question: ")

    mod = groq_moderate_prompt(query)

    while mod["violation"] == 1:
        print("\n❌ Question refused due to policy violation.")
        print(f"Category: {mod.get('category')}")
        print(f"Rationale: {mod.get('rationale')}")
        query = input("\nEnter a new question: ")
        mod = groq_moderate_prompt(query)

    if query.lower() == 'exit':
        print("Goodbye!")
        break

    if query.lower() == '/toggle':
        rag_mode_on = not rag_mode_on
        state = "ENABLED" if rag_mode_on else "DISABLED"
        print(f"*** RAG Mode is now {state} ***")
        continue
    try:
        print("Thinking...")

        if rag_mode_on:
            # Use the RAG pipeline with the 10-answer format
            response = qa_chain.invoke({"question": query})
            print("\n--- 10 Distinct Proposals (Based on Data) ---")
            print(response['result'])
        else:
            # GENERAL CHAT MODE — 10 independent answers
            answers = generate_multiple_answers(pure_llm, query, n=10)

            all_generated_answers.append(answers)

            print("\n--- 10 Diverse Answers ---")
            for i, ans in enumerate(answers, 1):
                print(f"{i}. {ans}")

            # Moderation step
            with open("answers_log.json", "w") as f:
                json.dump(all_generated_answers, f, indent=4)

                # Moderate all generated answers
                for answers in all_generated_answers:
                    moderation_results = moderate_multiple_texts(answers)
    except Exception as e:
        print(f"An error occurred: {e}")
