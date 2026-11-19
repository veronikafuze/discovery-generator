# 🧠 Discovery Generator

### An AI tool for uncovering non-obvious connections between scientific papers

[![Python](https://img.shields.io/badge/Python-3.10–3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/Local_LLM-Ollama-black?style=for-the-badge)](https://ollama.com)
[![arXiv](https://img.shields.io/badge/Data-arXiv-B31B1B?style=for-the-badge)](https://arxiv.org)

---

**Discovery Generator** helps researchers save dozens of hours of routine work. The tool automatically downloads fresh papers from arXiv, finds semantically close pairs from different research fields, and uses large language models (LLMs) to generate ready-to-use research hypotheses at their intersection.

> **Tested on:** Windows 10/11, Python 3.14, Ollama 0.40. To check your Windows version, press `Win + R`, type `winver` and press Enter. On Mac/Linux the steps below also work, but the activate command differs (see step 2).

## ⚙️ How it works

The pipeline consists of three simple steps:

1. **Data collection:** The script `1_fetch_papers.py` downloads paper abstracts for two specified categories.
2. **Connection search:** The script `2_embed_and_find_pairs.py` converts the texts into vector embeddings and finds pairs with high semantic similarity.
3. **Hypothesis generation:** The script `3_generate_hypotheses.py` sends the found pairs to the neural network to formulate a research idea, its rationale, and a method for testing it.

## 🚀 Quick start

```bash
# 1. Get the repository: either clone it...
git clone https://github.com/veronikafuze/discovery-generator.git
cd discovery-generator
# ...or download it as a ZIP (green "Code" button → "Download ZIP") and unzip it.
```

> **Note on the Python version:** the project is tested on Python 3.10–3.14. On the very newest Python (3.15) `pip install` may fail with `Failed building wheel for pyyaml` — if that happens, install Python 3.14 from [python.org](https://www.python.org/downloads/) and recreate the environment with `py -3.14 -m venv venv`.

```bash
# 2. Create a virtual environment
python -m venv venv
# For Windows:
venv\Scripts\activate
# For Mac/Linux:
source venv/bin/activate

# 3. Install the dependencies
pip install -r requirements.txt

# 4. Install Ollama (https://ollama.com) and the model
ollama run llama3.2

# 5. Run the download and connection search
python 1_fetch_papers.py
python 2_embed_and_find_pairs.py

# 6. Run the hypothesis generation
python 3_generate_hypotheses.py
```

> **Note on timing:** step 6 is the slowest one — the model needs about 1–2 minutes per paper pair, so the whole generation can take 15–20 minutes. The window may look "frozen" with a blinking cursor: this is normal, just wait. Steps 1 and 2 take 1–3 minutes each.

> **Note on the model name:** the config file expects a model named `my-llama` (see `OLLAMA_MODEL` in `config.py`). The easiest fix: run `ollama cp llama3.2 my-llama` right after installing — this creates a copy of the model under the expected name. Alternatively, set `OLLAMA_MODEL = "llama3.2"` in `config.py`.

> If the model download fails with a network error (e.g., `TLS handshake timeout`), simply run `ollama run llama3.2` again — the failure is usually temporary. If it keeps failing, see the fallback method below.

## 📦 Fallback: importing the model manually

If Ollama cannot download the model from its server (repeated network errors), you can load it from a file instead. This path gives the model the name `my-llama` right away, so step `ollama cp` is **not needed** — skip it.

1. **Download the model file.** In your browser, open `https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF`, find the file `Meta-Llama-3.2-3B-Instruct-Q4_K_M.gguf` (~2 GB) in the "Files" section and download it.
2. **Create a Modelfile.** In the project folder, create a new text file with a single line pointing to where you saved the downloaded file:
   ```
   FROM C:\Users\<YourName>\Downloads\Meta-Llama-3.2-3B-Instruct-Q4_K_M.gguf
   ```
   Replace the path with your own: right-click the downloaded file → "Copy as path" → paste. Save the file as `Modelfile.txt` in the project folder.
3. **Build the model in Ollama.** In the terminal (inside the project folder):
   ```bash
   ollama create my-llama -f Modelfile.txt
   ```
4. **Check it worked:**
   ```bash
   ollama list
   ```
   `my-llama` should appear in the list. Then continue from step 5 of the Quick start.

## 🎯 Choosing research fields

By default, the tool looks for connections between **neuroscience** (`q-bio.NC`) and **machine learning** (`cs.LG`). You can easily change the topics in the `config.py` file.

Where to find other categories? The full list is available in the [official arXiv catalog](https://arxiv.org/category_taxonomy).

Examples of interesting combinations for experiments:

* `cs.CL` (Computational Linguistics) + `econ.GN` (Economics)
* `q-bio.QM` (Quantitative Biology) + `physics.chem-ph` (Chemical Physics)
* `cond-mat.mtrl-sci` (Materials Science) + `cs.AI` (Artificial Intelligence)

## 🤖 Local or cloud-based model?

The `config.py` file contains the `LLM_BACKEND` setting.

**Option 1: Local (default, free).**
Uses `Ollama` on your machine. No data leaves your network. Make sure you have the model installed (see the Quick start section above).

**Option 2: Cloud (planned).**
Support for free cloud APIs (e.g., Groq) is planned for upcoming versions. For now, please use the local mode.

## 📄 Output

Once all the scripts have run successfully, a file named **`hypotheses_report.md`** will appear in the `output/` folder — a nicely formatted report with the generated hypotheses and links to the source papers.

---

*Author: [Veronika Fuzeinikova](https://github.com/veronikafuze).*
