import pandas as pd
from openai import OpenAI
import streamlit as st

# --- Load data ---
df = pd.read_csv("education_code_48.csv")

# --- Setup OpenAI client ---
client = OpenAI()

# --- Page config ---
st.set_page_config(page_title="Texas Education Code Q&A", page_icon="🎓")

st.title("🎓 Texas Education Code Chapter 48 Q&A")
st.write("Ask about any section, keyword, or topic (e.g., 'Sec. 48.003', 'eligibility', or 'funding').")

# --- Search box ---
query = st.text_input("Your question:")

def explain_in_plain_english(text):
    prompt = f"Explain this Texas education law section in plain, simple English (1–2 sentences):\n\n{text}"
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You explain Texas law clearly and simply for non-lawyers."},
            {"role": "user", "content": prompt}
        ],
    )
    return completion.choices[0].message.content.strip()

# --- Run search ---
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
            st.markdown(f"[View Full Text Online]({row['url']})")
            with st.expander("Plain English Explanation"):
                st.write(explain_in_plain_english(row['text']))
