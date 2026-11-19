🧠 Discovery Generator
ИИ-инструмент для поиска неочевидных связей между научными статьями
https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge
https://img.shields.io/badge/Local_LLM-Ollama-black?style=for-the-badge
https://img.shields.io/badge/Data-arXiv-B31B1B?style=for-the-badge

Discovery Generator помогает исследователям экономить десятки часов рутины. Инструмент автоматически скачивает свежие статьи из arXiv, находит семантически близкие пары из разных научных областей и генерирует на их стыке готовые исследовательские гипотезы с помощью больших языковых моделей (LLM).

⚙️ Как это работает
Пайплайн состоит из трёх простых шагов:

Сбор данных: Скрипт 1_fetch_papers.py скачивает абстракты статей по двум заданным категориям.

Поиск связей: Скрипт 2_embed_and_find_pairs.py переводит тексты в векторное представление и находит пары с высоким смысловым сходством.

Генерация гипотез: Скрипт 3_generate_hypotheses.py отправляет найденные пары нейросети для формулирования научной идеи, обоснования и метода проверки.

🚀 Быстрый старт
bash
# 1. Клонируйте репозиторий
git clone https://github.com/veronikafuze/discovery-generator.git
cd discovery-generator

# 2. Создайте виртуальное окружение
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для Mac/Linux:
source venv/bin/activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Запустите скачивание и поиск связей
python 1_fetch_papers.py
python 2_embed_and_find_pairs.py

# 5. Запустите генерацию гипотез
python 3_generate_hypotheses.py
🎯 Настройка научных областей
По умолчанию инструмент ищет связь между нейробиологией (q-bio.NC) и машинным обучением (cs.LG). Вы можете легко поменять темы в файле config.py.

Где взять другие категории? Полный список доступен в официальном каталоге arXiv.

Примеры интересных связок для экспериментов:

cs.CL (Компьютерная лингвистика) + econ.GN (Экономика)

q-bio.QM (Количественная биология) + physics.chem-ph (Химическая физика)

cond-mat.mtrl-sci (Материаловедение) + cs.AI (Искусственный интеллект)

🤖 Локальная или облачная нейросеть?
В файле config.py есть настройка LLM_BACKEND. Вы можете выбрать один из двух режимов.

Вариант 1: Локально (по умолчанию, бесплатно).
Использует Ollama на вашем компьютере. Никакие данные не уходят в сеть. Убедитесь, что у вас установлена модель llama3.2.

Вариант 2: Облако (быстрее, если ноутбук слабый).
Используйте бесплатные API (например, Groq). Получите ключ на console.groq.com и впишите его в config.py.

📄 Результат
После успешного выполнения всех скриптов, в папке output/ появится файл hypotheses_report.md — красивый отчёт с 10 сгенерированными гипотезами и ссылками на исходные статьи.

Автор: Veronika Fuzeinikova.
