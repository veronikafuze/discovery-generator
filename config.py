# Какие две разные области скрещиваем.
CATEGORY_A = "q-bio.NC"   # Нейробиология (Neurons and Cognition)
CATEGORY_B = "cs.LG"      # Машинное обучение (Machine Learning)

# Сколько статей качать из каждой области
MAX_PAPERS_PER_CATEGORY = 150

# Порог сходства (0.6-0.75 - оптимально)
SIMILARITY_THRESHOLD = 0.35

# Сколько пар гипотез сгенерировать
NUM_HYPOTHESES = 10

# === Выбор LLM для генерации гипотез ===
# Вариант 1: "ollama" — бесплатно локально (сложнее)
# Вариант 2: "groq" — бесплатный API с лимитами (проще)
LLM_BACKEND = "ollama"

# Для Groq (если выбрал LLM_BACKEND = "groq")
# Получи бесплатный ключ на https://console.groq.com/keys
GROQ_API_KEY = "вставьте свой ключ"
GROQ_MODEL = "llama-3.1-8b-instant"

# Для Ollama (если выбрал "ollama")
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "my-llama"
# Для Polza.ai
POLZA_API_KEY = "вставьте свой ключ"
POLZA_MODEL = "meta-llama/llama-3.1-8b-instruct" 
# Для ZvenoAI
ZVENO_API_KEY = "вставьте свой ключ"
ZVENO_MODEL = "nvidia/nemotron-3.5-lightning:free"