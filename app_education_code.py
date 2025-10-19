import pandas as pd
from openai import OpenAI
import streamlit as st

client = OpenAI()
df = pd.read_csv("education_code_48.csv")

st.title("Texas Education Code Chapter 48 Q&A")
query = st.text_input("Enter a keyword or section number:")

def explain_in_plain_english(text):
    prompt = f"Explain this Texas education law section in plain, simple English (1–2 sentences):\n\n{text}"
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You explain Texas law in plain English for non-lawyers."},
            {"role": "user", "content": prompt}
        ],
    )
    return completion.choices[0].message.content.strip()

if query:
    results = df[
        df["section"].str.lower().str.contains(query.lower(), na=False)
        | df["title"].str.lower().str.contains(query.lower(), na=False)
        | df["text"].str.lower().str.contains(query.lower(), na=False)
    ]
    if results.empty:
        st.warning("No matching sections found.")
    else:
        for _, row in results.iterrows():
            st.subheader(f"{row['section']} – {row['title']}")
            st.write(row['text'][:800] + "...")
            st.write(f"[View on Website]({row['url']})")
            st.info(explain_in_plain_english(row['text']))
