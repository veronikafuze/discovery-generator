import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import CATEGORY_A, CATEGORY_B, SIMILARITY_THRESHOLD

print("=== Шаг 2: Эмбеддинги и поиск пар ===")
df = pd.read_csv("output/papers.csv")
print(f"Загружено {len(df)} статей.")

print("Загружаю модель эмбеддингов (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = (df["title"] + ". " + df["abstract"]).tolist()
print("Считаю эмбеддинги (может занять 1-2 минуты на CPU)...")
embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
df["embedding_idx"] = range(len(df))

mask_a = df["category"] == CATEGORY_A
mask_b = df["category"] == CATEGORY_B
emb_a = embeddings[mask_a.values]
emb_b = embeddings[mask_b.values]
df_a = df[mask_a].reset_index(drop=True)
df_b = df[mask_b].reset_index(drop=True)

print(f"Сравниваю {len(df_a)} × {len(df_b)} пар...")
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
    print(f"\n✅ Найдено {len(pairs_df)} пар с similarity ≥ {SIMILARITY_THRESHOLD}")
    print("\nТоп-3 пары для проверки:")
    for _, row in pairs_df.head(3).iterrows():
        print(f"\n  [{row['similarity']}]")
        print(f"  A: {row['paper_a_title'][:80]}")
        print(f"  B: {row['paper_b_title'][:80]}")
else:
    print(f"\n⚠️ Пар не найдено. Ни одна статья не набрала {SIMILARITY_THRESHOLD} сходства.")
    print("Пожалуйста, открой файл config.py и снизь SIMILARITY_THRESHOLD до 0.30, затем запусти скрипт снова.")