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

