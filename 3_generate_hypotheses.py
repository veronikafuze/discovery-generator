import pandas as pd
import requests
import json
import os
from config import NUM_HYPOTHESES, OLLAMA_URL, OLLAMA_MODEL

os.makedirs("output", exist_ok=True)

PROMPT_TEMPLATE = """You are a scientific futurist working at the intersection of disciplines.
You are given two papers from DIFFERENT fields. Find a non-obvious yet logical connection between them and formulate ONE testable research hypothesis.

Paper A:
Title: {title_a}
Abstract: {abstract_a}

Paper B:
Title: {title_b}
Abstract: {abstract_b}

Answer strictly in the following format (no markdown, no introductions):

HYPOTHESIS: <one sentence — what if we apply X from paper A to problem Y from paper B>

RATIONALE: <2-3 sentences on why this could work — what shared structure/principle exists in both works>

HOW TO TEST: <1-2 concrete experiments or metrics to verify the hypothesis>

NOVELTY: <1 sentence — why this may be non-obvious to specialists from both fields>
"""

def call_ollama(prompt: str) -> str:
    try:
        # Send the request to the local Ollama instance
        r = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7},
        }, timeout=900)
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        return f"[Ollama ERROR: {e}]"

if __name__ == "__main__":
    print("=== Step 3: Generating hypotheses with the local Ollama model ===")
    pairs_df = pd.read_csv("output/pairs.csv")
    pairs_df = pairs_df.head(NUM_HYPOTHESES)
    
    results = []
    for i, row in pairs_df.iterrows():
        print(f"\n[{i+1}/{len(pairs_df)}] similarity={row['similarity']}")
        print("  ⏳ The local neural network is thinking (this may take 1-2 minutes)...")
        
        prompt = PROMPT_TEMPLATE.format(
            title_a=row["paper_a_title"],
            abstract_a=row["paper_a_abstract"][:500],
            title_b=row["paper_b_title"],
            abstract_b=row["paper_b_abstract"][:500],
        )
        
        answer = call_ollama(prompt)
        print(answer[:900] + "...") # Show the first lines of the response
        
        results.append({
            "similarity": row["similarity"],
            "paper_a_title": row["paper_a_title"],
            "paper_a_url": row["paper_a_url"],
            "paper_b_title": row["paper_b_title"],
            "paper_b_url": row["paper_b_url"],
            "hypothesis": answer,
        })

    out_df = pd.DataFrame(results)
    out_df.to_csv("output/hypotheses.csv", index=False)

    with open("output/hypotheses_report.md", "w", encoding="utf-8") as f:
        f.write("# Generated cross-disciplinary hypotheses\n\n")
        for i, row in out_df.iterrows():
            f.write(f"## Hypothesis {i+1} (similarity={row['similarity']})\n\n")
            f.write(f"**Paper A:** [{row['paper_a_title']}]({row['paper_a_url']})\n\n")
            f.write(f"**Paper B:** [{row['paper_b_title']}]({row['paper_b_url']})\n\n")
            f.write(f"{row['hypothesis']}\n\n---\n\n")

    print(f"\n✅ Done! {len(out_df)} hypotheses saved to output/hypotheses_report.md")
