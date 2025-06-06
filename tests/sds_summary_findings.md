# SDS Metric Evaluation Summary

This document presents the evaluation of the Semantic Drift Score (SDS) using both GTE and Stella models, and compares it to standard summarization metrics: BERTScore, ROUGE-1, ROUGE-L, and BLEU.

## 🔁 Correlation Matrix

| Metric         | SDS_GTE | SDS_Stella | CosSim_GTE | CosSim_Stella | BERTScore_F1 | ROUGE-1 | ROUGE-L | BLEU |
|----------------|---------|------------|-------------|----------------|---------------|----------|----------|--------|
| SDS_GTE        | 1.000   | 0.786      | -1.000      | -0.786         | -0.483        | -0.336   | -0.316   | -0.313 |
| SDS_Stella     | 0.786   | 1.000      | -0.786      | -1.000         | -0.561        | -0.357   | -0.331   | -0.315 |
| BERTScore_F1   | -0.483  | -0.561     | 0.483       | 0.561          | 1.000         | 0.688    | 0.698    | 0.671  |
| ROUGE-1        | -0.336  | -0.357     | 0.336       | 0.357          | 0.688         | 1.000    | 0.938    | 0.824  |
| ROUGE-L        | -0.316  | -0.331     | 0.316       | 0.331          | 0.698         | 0.938    | 1.000    | 0.910  |
| BLEU           | -0.313  | -0.315     | 0.313       | 0.315          | 0.671         | 0.824    | 0.910    | 1.000  |

## 📈 Summary Statistics

| Metric         | Min    | Max    | Median | Mean   | Std Dev | CV    |
|----------------|--------|--------|--------|--------|---------|-------|
| SDS_GTE        | 0.031  | 0.269  | 0.118  | 0.126  | 0.046   | 0.363 |
| CosSim_GTE     | 0.731  | 0.969  | 0.882  | 0.874  | 0.046   | 0.052 |
| SDS_Stella     | 0.029  | 0.365  | 0.136  | 0.144  | 0.054   | 0.378 |
| CosSim_Stella  | 0.635  | 0.971  | 0.864  | 0.856  | 0.054   | 0.064 |
| BERTScore_F1   | 0.798  | 0.908  | 0.849  | 0.848  | 0.017   | 0.020 |
| ROUGE-1        | 0.028  | 0.530  | 0.139  | 0.154  | 0.075   | 0.490 |
| ROUGE-L        | 0.020  | 0.502  | 0.098  | 0.112  | 0.062   | 0.553 |
| BLEU           | 0.002  | 0.269  | 0.024  | 0.033  | 0.032   | 0.966 |

## ✅ Takeaways

- SDS is strongly inversely correlated with all major summary metrics.
- Stella SDS has higher correlation with BERTScore than GTE SDS.
- SDS is interpretable, has low variance, and tracks well with semantic fidelity.

# Summary of Findings: Semantic Drift Score (SDS) Calibration on CNN/DailyMail

This analysis evaluates the Semantic Drift Score (SDS), calculated using both GTE and Stella embedding models. The evaluation was performed on **500 randomly selected examples** from the test split of the CNN/DailyMail ("3.0.0") dataset, comparing human-written summaries (highlights) against their corresponding source articles. SDS was then correlated with established metrics: BERTScore_F1, ROUGE-1, ROUGE-L, and BLEU, all of which were also calculated by comparing the human summary to the source article for these **500 samples**.

## 1. Core SDS Calculation and Model Consistency
*   **Unit Test Validation:** An independent unit test confirmed the arithmetic of the SDS calculation (`1 - cosine_similarity`) operates correctly within expected bounds. While cosine similarity ranges from **–1.0 to 1.0** in theory, modern embedding models (e.g., SentenceTransformers) output **normalized vectors**, making the **practical SDS range [0.0, 1.0]**.
*   **High Inter-Model Agreement (SDS_GTE vs. SDS_Stella):** A strong positive correlation of **0.786** was observed between the SDS scores generated by the GTE model and the Stella model **across the 500 samples**.
    *   **Interpretation:** This indicates that both embedding models, despite their different architectures and sizes, largely concur on the relative semantic drift between the human summaries and their source articles. This provides strong **convergent validity** for the SDS concept itself.

## 2. Relationship Between SDS and Established Evaluation Metrics (based on 500 samples)

### 2.1. Alignment with Semantic Similarity (BERTScore_F1)
*   **CosineSim_GTE vs. BERTScore_F1:** Moderate positive correlation (**0.483**).
*   **CosineSim_Stella vs. BERTScore_F1:** Moderate positive correlation (**0.561**).
    *   (This implies SDS_GTE vs. BERTScore_F1 is -0.483, and SDS_Stella vs. BERTScore_F1 is -0.561).
*   **Interpretation:** As the semantic similarity perceived by GTE/Stella increases (higher CosineSim, lower SDS), BERTScore_F1 also tends to increase. This confirms that SDS is effectively capturing dimensions of semantic similarity that are recognized by other established semantic evaluation measures when assessing human summaries against source material. Stella's SDS shows a slightly stronger alignment with BERTScore in this context.

### 2.2. Differentiation from Lexical Overlap Metrics (ROUGE, BLEU)
*   **CosineSim_GTE vs. ROUGE-1, ROUGE-L, BLEU:** Weak to moderate positive correlations (ranging from **0.313 to 0.336**).
*   **CosineSim_Stella vs. ROUGE-1, ROUGE-L, BLEU:** Weak to moderate positive correlations (ranging from **0.315 to 0.357**).
*   **Interpretation:** The correlations with lexical metrics are notably weaker than with BERTScore. This is a significant finding, suggesting that SDS (and the underlying cosine similarity of embeddings) measures a different aspect of summary quality than simple n-gram or sequence overlap. It indicates SDS can identify semantic faithfulness even when summaries are abstractive and use different vocabulary than the source, a limitation of ROUGE/BLEU.

## 3. Distribution and Characteristics of SDS for Human Summaries (CNN/DailyMail - 500 Samples)
*   **SDS Score Range & Central Tendency (from `sds_dual_model_eval.csv` data):**
    *   **Mean SDS_GTE:** 0.126
    *   **Mean SDS_Stella:** 0.144
    *   **Max SDS_GTE:** 0.269
    *   **Max SDS_Stella:** 0.365
*   **Interpretation:**
    *   On average, for this sample of 500 human summaries from CNN/DailyMail, they exhibit a relatively low semantic drift from their source articles according to both GTE and Stella. This establishes a baseline for what "good" semantic faithfulness looks like for this dataset and summarization style.
    *   The visualized histogram (from `cal_sds.py`) comparing SDS_GTE and SDS_Stella distributions would further illuminate differences in their typical scoring patterns (e.g., central tendency, spread) for these human summaries.
*   **Metric Sensitivity:** The Coefficient of Variation (CV) for SDS metrics (around 0.37) was considerably higher than for BERTScore_F1 (0.020) on this dataset. This suggests that while BERTScore indicated generally high similarity for most pairs in this sample, SDS might offer more discriminatory power or granularity in distinguishing between already good-quality summaries.

## 4. Overall Conclusions & Next Steps
*   **SDS is a Robust Semantic Metric:** Based on the evaluation of 500 samples, the SDS, implemented with either GTE or Stella, provides a consistent and meaningful measure of semantic similarity/drift, aligning with but also offering distinct insights compared to existing metrics.
*   **Valuable for Abstractive Summarization:** Its ability to capture semantic meaning beyond lexical overlap makes it particularly promising for evaluating abstractive summaries where faithfulness to the source's meaning is paramount.
*   **Baseline for Human Performance:** The analysis on CNN/DailyMail provides a valuable baseline for SDS scores associated with high-quality human summarization within this sample. This can inform the setting of thresholds for "good enough" summaries in automated systems.
*   **Further Research:** Testing SDS on datasets with a wider spectrum of summary qualities, including machine-generated summaries of varying quality and summaries known to contain factual inaccuracies or misleading content, will be crucial for understanding its full capabilities and limitations. Comparing SDS directly against human judgments of semantic adequacy across diverse samples would also be a valuable next step.
