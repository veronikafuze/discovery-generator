import pandas as pd
import requests
import json
import os
from config import NUM_HYPOTHESES, OLLAMA_URL, OLLAMA_MODEL

os.makedirs("output", exist_ok=True)

PROMPT_TEMPLATE = """Ты — научный футуролог на стыке дисциплин.
Тебе даны две статьи из РАЗНЫХ областей. Найди неочевидную, но логичную связь между ними и сформулируй ОДНУ проверяемую исследовательскую гипотезу.

Статья A:
Заголовок: {title_a}
Абстракт: {abstract_a}

Статья B:
Заголовок: {title_b}
Абстракт: {abstract_b}

Ответь строго в таком формате (без markdown, без вступлений):

ГИПОТЕЗА: <одно предложение — что если применить X из статьи A к проблеме Y из статьи B>

ОБОСНОВАНИЕ: <2-3 предложения, почему это может работать — какая общая структура/принцип есть в обеих работах>

КАК ПРОВЕРИТЬ: <1-2 конкретных эксперимента или метрики, которыми можно проверить гипотезу>

НОВИЗНА: <1 предложение — почему это может быть неочевидно для специалистов из обеих областей>
"""

def call_ollama(prompt: str) -> str:
    try:
        # Отправляем запрос локально в Олламу
        r = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7},
        }, timeout=900)
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        return f"[ОШИБКА Ollama: {e}]"

if __name__ == "__main__":
    print("=== Шаг 3: Генерация гипотез через локальную модель Ollama ===")
    pairs_df = pd.read_csv("output/pairs.csv")
    pairs_df = pairs_df.head(NUM_HYPOTHESES)
    
    results = []
    for i, row in pairs_df.iterrows():
        print(f"\n[{i+1}/{len(pairs_df)}] similarity={row['similarity']}")
        print("  ⏳ Локальная нейросеть думает (это может занять 1-2 минуты)...")
        
        prompt = PROMPT_TEMPLATE.format(
            title_a=row["paper_a_title"],
            abstract_a=row["paper_a_abstract"][:500],
            title_b=row["paper_b_title"],
            abstract_b=row["paper_b_abstract"][:500],
        )
        
        answer = call_ollama(prompt)
        print(answer[:900] + "...") # Показываем первые строчки ответа
        
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
        f.write("# Сгенерированные междисциплинарные гипотезы\n\n")
        for i, row in out_df.iterrows():
            f.write(f"## Гипотеза {i+1} (similarity={row['similarity']})\n\n")
            f.write(f"**Статья A:** [{row['paper_a_title']}]({row['paper_a_url']})\n\n")
            f.write(f"**Статья B:** [{row['paper_b_title']}]({row['paper_b_url']})\n\n")
            f.write(f"{row['hypothesis']}\n\n---\n\n")

    print(f"\n✅ Готово! {len(out_df)} гипотез сохранены в output/hypotheses_report.md")