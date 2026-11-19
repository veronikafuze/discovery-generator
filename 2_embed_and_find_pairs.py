import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import CATEGORY_A, CATEGORY_B, SIMILARITY_THRESHOLD

print("=== Step 2: Embeddings and pair search ===")
df = pd.read_csv("output/papers.csv")
print(f"Loaded {len(df)} papers.")

print("Loading the embedding model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = (df["title"] + ". " + df["abstract"]).tolist()
print("Computing embeddings (this may take 1-2 minutes on CPU)...")
embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
df["embedding_idx"] = range(len(df))

mask_a = df["category"] == CATEGORY_A
mask_b = df["category"] == CATEGORY_B
emb_a = embeddings[mask_a.values]
emb_b = embeddings[mask_b.values]
df_a = df[mask_a].reset_index(drop=True)
df_b = df[mask_b].reset_index(drop=True)

print(f"Comparing {len(df_a)} × {len(df_b)} pairs...")
sim_matrix = cosine_similarity(emb_a, emb_b)

pairs = []
for i in range(len(df_a)):
    j = int(np.argmax(sim_matrix[i]))
    score = float(sim_matrix[i, j])
    if score >= SIMILARITY_THRESHOLD:
        pairs.append({
            "similarity": round(score, 4),
            "paper_a_title": df_a.loc[i, "title"],
            "paper_a_abstract": df_a.loc[i, "abstract"],
            "paper_a_url": df_a.loc[i, "url"],
            "paper_b_title": df_b.loc[j, "title"],
            "paper_b_abstract": df_b.loc[j, "abstract"],
            "paper_b_url": df_b.loc[j, "url"],
        })

if len(pairs) > 0:
    pairs_df = pd.DataFrame(pairs).sort_values("similarity", ascending=False)
    pairs_df = pairs_df.drop_duplicates(subset=["paper_b_url"])
    pairs_df.to_csv("output/pairs.csv", index=False)
    print(f"\n✅ Found {len(pairs_df)} pairs with similarity ≥ {SIMILARITY_THRESHOLD}")
    print("\nTop-3 pairs for a quick check:")
    for _, row in pairs_df.head(3).iterrows():
        print(f"\n  [{row['similarity']}]")
        print(f"  A: {row['paper_a_title'][:80]}")
        print(f"  B: {row['paper_b_title'][:80]}")
else:
    print(f"\n⚠️ No pairs found. No paper scored a similarity of {SIMILARITY_THRESHOLD} or higher.")
    print("Please open config.py, lower SIMILARITY_THRESHOLD to 0.30, and run the script again.")
