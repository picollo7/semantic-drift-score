import unittest
from sentence_transformers import SentenceTransformer, util

class TestSemanticDriftScore(unittest.TestCase):

    def setUp(self):
        self.model = SentenceTransformer("Alibaba-NLP/gte-large-en-v1.5", trust_remote_code=True)
        self.original = "The cat sat on the mat and purred contentedly in the warm sunlight."
        self.summary = "A cat rested happily in the sun."

    def test_score_range(self):
        v0 = self.model.encode(self.original, convert_to_tensor=True, normalize_embeddings=True)
        v1 = self.model.encode(self.summary, convert_to_tensor=True, normalize_embeddings=True)
        cosine_sim = util.cos_sim(v0, v1).item()
        drift_score = 1 - cosine_sim

        print(f"Cosine Similarity: {cosine_sim:.4f}")
        print(f"Semantic Drift Score: {drift_score:.4f}")

        self.assertGreaterEqual(cosine_sim, -1.0)
        self.assertLessEqual(cosine_sim, 1.0)
        self.assertGreaterEqual(drift_score, 0.0)
        self.assertLessEqual(drift_score, 2.0)  # Just in case of unusual rounding

if __name__ == '__main__':
    unittest.main()
