# Context & Skill Sheet: SITANPAS Recommendation Engine

## 1. Project Overview
SITANPAS (Sistem Informasi & E-Commerce Hasil Laut) menggunakan engine Information Retrieval (IR) berbasis Content-Based Filtering untuk mencocokkan kueri pencarian pengguna dengan katalog produk UMKM perikanan.

## 2. Core Mathematical Rules
1. Feature Combining: Dokumen dibangun dari 3 kolom:
   D_i = nama_produk + " " + kategori + " " + deskripsi
2. Text Preprocessing: Case Folding -> Tokenization -> Filtering (Stopwords Perikanan) -> Stemming (Sastrawi).
3. TF-IDF & Cosine Similarity:
   - Vektor Kueri = (A)
   - Vektor Dokumen Produk = (B)
   - Scoring = Cosine Similarity (Sc)
4. Threshold Filtering: Cut-off kelayakan tampilan antarmuka pada Sc >= 0.34 (34%).

## 3. Evaluation Rules (Bab IV Experiment)
- Metrik Evaluasi: Precision, Recall, F1-Score, MRR, dan Hit Rate@k.
- Trigger Iterasi: Jika rata-rata F1-Score < Target pada pengujian offline, Peneliti (Lukman) melakukan kalibrasi custom stopwords/stemmer rules.
- Baseline Engine: Exact Match (Keyword Search konvensional).