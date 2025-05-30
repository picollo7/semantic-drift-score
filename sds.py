from sentence_transformers import SentenceTransformer, util
import argparse

MODEL_NAME = "Alibaba-NLP/gte-large-en-v1.5"
model = SentenceTransformer(MODEL_NAME, trust_remote_code=True)

def compute_drift_score(original_text: str, summary_text: str):
    v0 = model.encode(original_text, convert_to_tensor=True, normalize_embeddings=True)
    v1 = model.encode(summary_text, convert_to_tensor=True, normalize_embeddings=True)

    cosine_sim = util.cos_sim(v0, v1).item()
    drift_score = 1 - cosine_sim

    return {
        "cosine_similarity": round(cosine_sim, 4),
        "semantic_drift_score": round(drift_score, 4)
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

    result = compute_drift_score(original_text, summary_text)
    print("Cosine Similarity:", result["cosine_similarity"])
    print("Semantic Drift Score:", result["semantic_drift_score"])
