# 🧠 Discovery Generator

### An AI tool for uncovering non-obvious connections between scientific papers

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/Local_LLM-Ollama-black?style=for-the-badge)](https://ollama.com)
[![arXiv](https://img.shields.io/badge/Data-arXiv-B31B1B?style=for-the-badge)](https://arxiv.org)

---

**Discovery Generator** helps researchers save dozens of hours of routine work. The tool automatically downloads fresh papers from arXiv, finds semantically close pairs from different research fields, and uses large language models (LLMs) to generate ready-to-use research hypotheses at their intersection.

## ⚙️ How it works

The pipeline consists of three simple steps:

1. **Data collection:** The script `1_fetch_papers.py` downloads paper abstracts for two specified categories.
2. **Connection search:** The script `2_embed_and_find_pairs.py` converts the texts into vector embeddings and finds pairs with high semantic similarity.
3. **Hypothesis generation:** The script `3_generate_hypotheses.py` sends the found pairs to the neural network to formulate a research idea, its rationale, and a method for testing it.

## 🚀 Quick start

```bash
# 1. Clone the repository
git clone https://github.com/veronikafuze/discovery-generator.git
cd discovery-generator

# 2. Create a virtual environment
python -m venv venv
# For Windows:
venv\Scripts\activate
# For Mac/Linux:
source venv/bin/activate

# 3. Install the dependencies
pip install -r requirements.txt

# 4. Run the download and connection search
python 1_fetch_papers.py
python 2_embed_and_find_pairs.py

# 5. Run the hypothesis generation
python 3_generate_hypotheses.py
```

## 🎯 Choosing research fields

By default, the tool looks for connections between **neuroscience** (`q-bio.NC`) and **machine learning** (`cs.LG`). You can easily change the topics in the `config.py` file.

Where to find other categories? The full list is available in the [official arXiv catalog](https://arxiv.org/category_taxonomy).

Examples of interesting combinations for experiments:

* `cs.CL` (Computational Linguistics) + `econ.GN` (Economics)
* `q-bio.QM` (Quantitative Biology) + `physics.chem-ph` (Chemical Physics)
* `cond-mat.mtrl-sci` (Materials Science) + `cs.AI` (Artificial Intelligence)

## 🤖 Local or cloud-based model?

The `config.py` file contains the `LLM_BACKEND` setting. You can choose between two modes.

**Option 1: Local (default, free).**
Uses `Ollama` on your machine. No data leaves your network. Make sure you have the `llama3.2` model installed.

**Option 2: Cloud (faster if your laptop is weak).**
Use free APIs (e.g., Groq). Get a key at [console.groq.com](https://console.groq.com) and paste it into `config.py`.

## 📄 Output

Once all the scripts have run successfully, a file named **`hypotheses_report.md`** will appear in the `output/` folder — a nicely formatted report with 10 generated hypotheses and links to the source papers.

---

*Author: [Veronika Fuzeinikova](https://github.com/veronikafuze).*
