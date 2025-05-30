# SDS Calibration Notebook (Dual Model: GTE & Stella)
# Goal: Evaluate Semantic Drift Score (SDS) using both GTE and Stella + compare to BERTScore, ROUGE, BLEU

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer, util
from datasets import load_dataset
from bert_score import score as bert_score
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Load a summarization benchmark dataset
# cnn_dailymail has fields 'article' (source) and 'highlights' (summary)
data = load_dataset("cnn_dailymail", "3.0.0")
examples = data['test'].shuffle(seed=42).select(range(500))

# Load SDS models
gte_model = SentenceTransformer("Alibaba-NLP/gte-large-en-v1.5", trust_remote_code=True)
stella_model = SentenceTransformer("NovaSearch/stella_en_400M_v5", trust_remote_code=True)

rouge = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
smoothie = SmoothingFunction().method4


def compute_sds(model, original, summary):
    v0 = model.encode(original, convert_to_tensor=True, normalize_embeddings=True)
    v1 = model.encode(summary, convert_to_tensor=True, normalize_embeddings=True)
    sim = util.cos_sim(v0, v1).item()
    return round(1 - sim, 4), round(sim, 4)

# Store scores and human references
records = []
for ex in examples:
    src = ex['article']
    ref = ex['highlights']  # human-written summary
    sds_gte, cos_gte = compute_sds(gte_model, src, ref)
    sds_stella, cos_stella = compute_sds(stella_model, src, ref)

    P, R, F1 = bert_score([ref], [src], lang="en", verbose=False)
    rouge_scores = rouge.score(ref, src)
    bleu = sentence_bleu([ref.split()], src.split(), smoothing_function=smoothie)

    records.append({
        'source': src,
        'reference': ref,
        'SDS_GTE': sds_gte,
        'CosineSim_GTE': cos_gte,
        'SDS_Stella': sds_stella,
        'CosineSim_Stella': cos_stella,
        'BERTScore_F1': round(F1[0].item(), 4),
        'ROUGE-1': round(rouge_scores['rouge1'].fmeasure, 4),
        'ROUGE-L': round(rouge_scores['rougeL'].fmeasure, 4),
        'BLEU': round(bleu, 4),
        'Length': len(ref.split())
    })

# Convert to DataFrame
df = pd.DataFrame(records)

# Visualize SDS Distribution Comparison
plt.figure(figsize=(10, 5))
plt.hist(df['SDS_GTE'], bins=20, alpha=0.5, label='GTE', edgecolor='black')
plt.hist(df['SDS_Stella'], bins=20, alpha=0.5, label='Stella', edgecolor='black')
plt.title("Semantic Drift Score Distribution on Human Summaries")
plt.xlabel("SDS (1 - Cosine Similarity)")
plt.ylabel("Count")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Correlation matrix
corr_matrix = df[['SDS_GTE', 'SDS_Stella', 'BERTScore_F1', 'ROUGE-1', 'ROUGE-L', 'BLEU']].corr()
print("\nCorrelation Matrix:")
print(corr_matrix)

# Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap of SDS vs Other Metrics")
plt.tight_layout()
plt.show()

# Save output for further analysis
df.to_csv("sds_dual_model_eval.csv", index=False)
