# Which two different research fields to cross.
CATEGORY_A = "q-bio.NC"   # Neuroscience (Neurons and Cognition)
CATEGORY_B = "cs.LG"      # Machine Learning

# How many papers to download from each field
MAX_PAPERS_PER_CATEGORY = 150

# Similarity threshold (0.6-0.75 is optimal)
SIMILARITY_THRESHOLD = 0.35

# How many hypotheses to generate
NUM_HYPOTHESES = 10

# === LLM backend selection ===
# Option 1: "ollama" — free and local (harder to set up)
# Option 2: "groq" — free API with rate limits (easier)
LLM_BACKEND = "ollama"

# For Groq (if you chose LLM_BACKEND = "groq")
# Get a free key at https://console.groq.com/keys
GROQ_API_KEY = "paste your key here"
GROQ_MODEL = "llama-3.1-8b-instant"

# For Ollama (if you chose "ollama")
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "my-llama"
# For Polza.ai
POLZA_API_KEY = "paste your key here"
POLZA_MODEL = "meta-llama/llama-3.1-8b-instruct" 
# For ZvenoAI
ZVENO_API_KEY = "paste your key here"
ZVENO_MODEL = "nvidia/nemotron-3.5-lightning:free"
