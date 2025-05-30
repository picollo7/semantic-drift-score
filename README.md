# semantic-drift-score

# SDS: Semantic Drift Score

SDS (Semantic Drift Score) is an open-source tool for quantifying **meaning loss during text compression**, such as summarization, by measuring the **embedding-based semantic difference** between an original text and its summary.

Built for clarity, extensibility, and liberation, SDS helps track, compare, and audit semantic preservation across compression strategies.

---

## 🔧 Features
- Compute cosine-based **semantic drift scores (SDS)**
- Compare results across different embedding models (e.g. GTE, Stella)
- Run single or dual-model analyses
- Command-line interface for automation
- Designed for long context support (up to 8192 tokens with current GTE and Stella models, you can change embedding models as desired)

---

## 📁 Project Structure

```text
sds/
├── sds.py                # Single-model CLI script
├── dual_sds.py           # Run SDS with two models side-by-side
├── requirements.txt      # Dependencies (sentence-transformers, torch, etc)
├── LICENSE               # GPL v3 License
├── README.md             # This file
├── examples/
│   ├── original.txt      # Example longform input
│   └── summary.txt       # Example compressed output
└── tests/
    └── test_sds.py       # Simple test suite for core functionality
```

---

## 🚀 Quick Start

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run with a single model:
```bash
python sds.py --original examples/original.txt --summary examples/summary.txt
```

### 3. Run with dual models (e.g., Stella and GTE):
```bash
python dual_sds.py --original examples/original.txt --summary examples/summary.txt
```

---

## 📐 What Is SDS?

Semantic Drift Score is defined as:

```python
SDS = 1 - cosine_similarity(embedding(original), embedding(summary))
```

This gives a **semantic difference score** from 0.0 (perfect retention) to ~1.0 (max drift).

Use cases include:
- **Compression quality tracking**
- **Summarization evaluation**
- **LLM memory audits**

---

## 📊 SDS Evaluation Summary

SDS (Semantic Drift Score) was benchmarked on 500 randomly sampled human summaries from the CNN/DailyMail dataset. Using both GTE and Stella embedding models, we evaluated its alignment with established metrics like BERTScore, ROUGE, and BLEU.

Key findings:
- ✅ **Strong inter-model agreement** between GTE and Stella SDS (r = 0.786)
- ✅ **Moderate inverse correlation** with BERTScore F1 (–0.48 to –0.56)
- ✅ **Low correlation with ROUGE/BLEU**, confirming SDS captures meaning, not just token overlap
- ✅ **Low SDS values (~0.13 avg)** on human summaries establish a baseline for “good” semantic fidelity

📄 See full writeup in [`docs/sds_summary_findings.md`](docs/sds_summary_findings.md)

---

## 🔒 License

This project is licensed under the GNU General Public License v3.0 (GPLv3). 
All derivative works must also remain free and open.

---

## 🌱 Contributing

Want to help calibrate SDS or improve model integration?
- Fork the repo
- Create a feature branch
- Submit a PR

Join the project’s liberation mission — SDS is part of a larger initiative to keep AI **transparent, inspectable, and free**.

---

## 🧪 Future Additions
- Optional chunking/rolling-window support for longer texts
- Compression-aware LLM memory scoring

---

## 🙏 Acknowledgments
- Stella by NovaSearch
- GTE by Alibaba
- sentence-transformers by UKPLab

And to everyone committed to building transparent, explainable, anti-enclosure AI tools.

---

## 📫 Contact
github.com/picollo7

---

**This is Fucking Bullshit-approved software.**

🌍 Free knowledge or nothing.

---
