# System Specification - SITANPAS IR Engine

## 1. Pipeline Komputasi

[Query Input] ------------------> [Preprocessing Query] ----> [Vektor TF-IDF (A)]
                                                                    |
                                                                    v
[Database (3 Cols)] -> [Feature Combining] -> [Preprocessing] -> [Vektor TF-IDF (B)]
                                                                    |
                                                                    v
                                                       [Cosine Similarity Calculation]
                                                                    |
                                                                    v
                                                       [Sorting & Threshold Sc >= 0.34]
                                                                    |
                                                                    v
                                                       [Output Top-N + Relevance Bar]

## 2. Technical Stack

- Environment: Python 3.x (Google Colab / VS Code)
- Libraries: pandas, numpy, scikit-learn (TfidfVectorizer, cosine_similarity), Sastrawi, matplotlib, seaborn.
