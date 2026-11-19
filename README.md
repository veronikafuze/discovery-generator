# Discovery Generator

ИИ-инструмент, который находит неочевидные связи между научными статьями и генерирует гипотезы с помощью локальной модели Ollama.

## Как запустить
1. Установите зависимости: `pip install -r requirements.txt`
2. Скачайте Ollama (https://ollama.com) и модель: `ollama run llama3.2`
3. Запустите скрипты по очереди: `1_fetch_papers.py`, `2_embed_and_find_pairs.py`, `3_generate_hypotheses.py`.