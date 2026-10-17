# src/metrics.py
import numpy as np

def calculate_precision_at_k(retrieved_ids, relevant_ids, k=10):
    """Menghitung Precision pada top-K hasil (Berapa banyak yang relevan dari yang ditampilkan)"""
    retrieved_k = retrieved_ids[:k]
    if not retrieved_k:
        return 0.0
    relevant_retrieved = set(retrieved_k).intersection(set(relevant_ids))
    return len(relevant_retrieved) / len(retrieved_k)

def calculate_recall(retrieved_ids, relevant_ids):
    """Menghitung Recall (Berapa banyak dokumen relevan yang berhasil ditemukan dari total seharusnya)"""
    if not relevant_ids:
        return 0.0
    relevant_retrieved = set(retrieved_ids).intersection(set(relevant_ids))
    return len(relevant_retrieved) / len(relevant_ids)

def calculate_f1_score(precision, recall):
    """Menghitung F1-Score (Harmonic mean dari Precision dan Recall)"""
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def calculate_mrr(retrieved_ids, relevant_ids):
    """Menghitung Mean Reciprocal Rank (MRR) - Seberapa cepat dokumen relevan PERTAMA ditemukan"""
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0

def calculate_hit_rate(retrieved_ids, relevant_ids):
    """Menghitung Hit Rate (Apakah ada minimal 1 dokumen relevan yang berhasil ditarik?)"""
    relevant_retrieved = set(retrieved_ids).intersection(set(relevant_ids))
    return 1.0 if len(relevant_retrieved) > 0 else 0.0