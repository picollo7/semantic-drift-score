import argparse
import torch
from sentence_transformers import SentenceTransformer, util
from concurrent.futures import ThreadPoolExecutor

stella_model = SentenceTransformer("NovaSearch/stella_en_400M_v5", trust_remote_code=True)
gte_model = SentenceTransformer("Alibaba-NLP/gte-large-en-v1.5", trust_remote_code=True)


def get_embedding(model, text):
    return model.encode(text, convert_to_tensor=True, normalize_embeddings=True)

def compute_drift_score(model, name, original, summary):
    v0 = get_embedding(model, original)
    v1 = get_embedding(model, summary)
    sim = util.cos_sim(v0, v1).item()
    return name, {
        "cosine_similarity": round(sim, 4),
        "semantic_drift_score": round(1 - sim, 4)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", type=str, required=True, help="Path to original text file")
    parser.add_argument("--summary", type=str, required=True, help="Path to summary text file")
    args = parser.parse_args()

    with open(args.original, 'r', encoding='utf-8') as f:
        original_text = f.read()
    with open(args.summary, 'r', encoding='utf-8') as f:
        summary_text = f.read()

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(compute_drift_score, gte_model, "GTE", original_text, summary_text),
            executor.submit(compute_drift_score, stella_model, "STELLA", original_text, summary_text)
        ]
        print("=== Semantic Drift Scores ===")
        for future in futures:
            name, result = future.result()
            print(f"{name}: {result}")
