import pandas as pd
from openai import OpenAI

# --- Load CSV ---
df = pd.read_csv("education_code_48.csv")

# --- Initialize GPT (you need an API key in your environment) ---
client = OpenAI()

print("Texas Education Code Chapter 48 Q&A System (with explanations)")
print("Type a keyword or section number (e.g. '48.003' or 'eligibility').")
print("Type 'exit' to quit.\n")

def explain_in_plain_english(text):
    """Ask GPT to summarize the section in plain English."""
    prompt = f"Explain this Texas education law section in plain, simple English (1–2 sentences):\n\n{text}"
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You explain Texas law in plain, clear English for non-lawyers."},
            {"role": "user", "content": prompt}
        ],
    )
    return completion.choices[0].message.content.strip()

def find_section(query):
    query = query.lower().strip()
    results = df[
        df["section"].str.lower().str.contains(query, na=False)
        | df["title"].str.lower().str.contains(query, na=False)
        | df["text"].str.lower().str.contains(query, na=False)
    ]
    return results

while True:
    q = input("Your question: ").strip()
    if q.lower() in ["exit", "quit"]:
        print("Exiting.")
        break

    result = find_section(q)
    if result.empty:
        print("No matching sections found.\n")
    else:
        for _, row in result.iterrows():
            print(f"\nSection: {row['section']} – {row['title']}")
            print(f"{row['text'][:600]}...")
            print(f"URL: {row['url']}\n")

            # Add plain English explanation
            summary = explain_in_plain_english(row['text'])
            print(f"Plain English Summary: {summary}\n")
