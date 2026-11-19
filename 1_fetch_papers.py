import arxiv
import pandas as pd
from tqdm import tqdm
from config import CATEGORY_A, CATEGORY_B, MAX_PAPERS_PER_CATEGORY
import os

os.makedirs("output", exist_ok=True)

def fetch_category(category: str, max_results: int) -> list[dict]:
    print(f"  Качаю {max_results} статей из категории '{category}'...")
    client = arxiv.Client(page_size=100, delay_seconds=3)
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    papers = []
    for result in tqdm(client.results(search), total=max_results):
        if not result.summary:
            continue
        papers.append({
            "id": result.entry_id.split("/")[-1],
            "title": result.title.strip().replace("\n", " "),
            "abstract": result.summary.strip().replace("\n", " "),
            "category": category,
            "authors": ", ".join(a.name for a in result.authors[:3]),
            "url": result.entry_id,
        })
    return papers

if __name__ == "__main__":
    print("=== Шаг 1: Скачивание статей ===")
    papers_a = fetch_category(CATEGORY_A, MAX_PAPERS_PER_CATEGORY)
    papers_b = fetch_category(CATEGORY_B, MAX_PAPERS_PER_CATEGORY)
    all_papers = papers_a + papers_b
    df = pd.DataFrame(all_papers).drop_duplicates(subset=["id"])
    df.to_csv("output/papers.csv", index=False)
    print(f"\n✅ Готово. Сохранено {len(df)} статей в output/papers.csv")
    print(f"   - {CATEGORY_A}: {len(papers_a)}")
    print(f"   - {CATEGORY_B}: {len(papers_b)}")