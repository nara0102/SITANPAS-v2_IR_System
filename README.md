# SITANPAS Information Retrieval (IR) Recommendation Engine

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Method-TF--IDF%20%2B%20Cosine%20Similarity-orange.svg)](README.md)

> **SITANPAS (Sistem Informasi & E-Commerce Hasil Laut)** — Module Engine Rekomendasi Produk Perikanan dan Olahan UMKM Pesisir berbasis *Content-Based Filtering* (CBF) dan *Information Retrieval* (IR).

---

## 📌 Deskripsi Proyek

`sitanpas-ir-system` merupakan mesin pencarian dan rekomendasi semantik berbasis *Information Retrieval* (IR) yang dirancang untuk platform e-commerce hasil laut pesisir **SITANPAS** di Desa Ambesia Selatan. Sistem ini mengatasi keterbatasan pencarian konvensional (*Exact Match*) dengan memanfaatkan pembobotan kata **TF-IDF (Term Frequency - Inverse Document Frequency)** dan pengukuran derajat kemiripan semantik **Cosine Similarity**.

Sistem ini mendukung variasi kueri pencarian kompleks, seperti:

- **Exact Keyword** (Pencarian kata kunci mutlak)
- **Synonym / Local Terms** (Istilah/sebutan daerah pesisir seperti *"Lure"*, *"Duo"*, *"Ikan Kering"*)
- **Typo / Spelling Errors** (Kueri dengan kesalahan ketik/fonetik seperti *"Trigiri"*, *"Chakalang"*)
- **Descriptive Query** (Kueri berbasis deskripsi/intensi penggunaan seperti *"teri kecil basah segar"*, *"ikan asin untuk digoreng"*)

---

## 🏗️ Pipeline Komputasi System Architecture

Sistem menggunakan alur pemrosesan data ganda (*Dual-Path Pipeline*) untuk kueri pengguna dan korpus dokumen produk:

```text
       [ JALUR QUERY PENGGUNA ]                     [ JALUR KORPUS DOKUMEN DATABASE ]
                  |                                                 |
                  v                                                 v
      [ Input Query Pencarian ]                       [ Database Produk SITANPAS ]
                  |                                  (nama_produk, kategori, deskripsi)
                  v                                                 |
     [ Preprocessing Teks Query ]                                   v
   - Case Folding                                     [ Feature Combining / Penggabungan ]
   - Tokenizing                                       (D = nama_produk + kategori + deskripsi)
   - Filtering (Stopword)                                           |
   - Stemming                                                       v
                  |                                   [ Preprocessing Teks Korpus ]
                  v                                   - Case Folding
     [ Matriks Vektor TF-IDF ]                        - Tokenizing
             (A)                                      - Filtering (Stopword)
                  |                                   - Stemming
                  |                                                 |
                  |                                                 v
                  |                                     [ Matriks Vektor TF-IDF ]
                  |                                                (B)
                  |                                                 |
                  +-----------------------+-------------------------+
                                          |
                                          v
                            [ Kalkulasi Cosine Similarity ]
                                          |
                                          v
                         [ Sorting & Threshold Filtering ]
                            (Penyaringan Sc >= 0.34)
                                          |
                                          v
                       [ Keluaran Rekomendasi Top-N ]
                      (Daftar Produk + Relevance Bar)
```

## Blueprint

sitanpas-ir-system/
│
├── .context/                   # Konteks AI Agent & Rules
│   └── GEMINI_SKILL.md         # Aturan main riset & variabel komputasi
│
├── docs/                       # Dokumentasi Spesifikasi & Metodologi
│   ├── SYSTEM_SPEC.md          # Spesifikasi arsitektur & komputasi IR
│   └── GROUND_TRUTH_SPEC.md    # Detail dataset 27 produk & 20 query uji
│
├── data/                       # Dataset Riil Supabase & Ground Truth
│   ├── produk.csv              # Catalog dataset produk (27 item)
│   └── ground_truth_SITANPAS.csv # Matriks kebenaran dasar 20 query uji
│
├── notebooks/                  # Eksperimen Evaluasi (BAB IV)
│   └── 01_ir_eval_sitanpas.ipynb
│
├── src/                        # Source Code Python Production Ready
│   ├── preprocessing.py        # Modul Text Preprocessing & Custom Stopwords
│   ├── tfidf_engine.py         # Modul Vectorization & Cosine Similarity
│   └── metrics.py              # Modul Evaluasi (Precision, Recall, F1, MRR, Hit Rate)
│
├── requirements.txt            # Dependensi pustaka Python
├── README.md                   # Dokumentasi Utama Proyek
└── LICENSE                     # Lisensi Hak Cipta

## 📊 Dataset & Ground Truth Specification

Korpus Data Utama: produk.csv (27 entri produk aktif dari Supabase)

Atribut Produk: product_id, nama_produk, kategori, deskripsi, harga, stok, satuan, berat_kg, nama_nelayan, lokasi_nelayan, status.

Query Uji Evaluasi: 20 Query Uji terbagi merata ke dalam 4 kategori karakteristik linguistik pesisir.

Metrik Evaluasi IR:

Precision@k

Recall@k

F1-Score

MRR (Mean Reciprocal Rank)

Hit Rate@k

## 👤 Peneliti & Kontributor

Peneliti utama: Lukman Hakim

Program Studi: S1 Teknik Informatika, Universitas Tadulako (Palu, Central Sulawesi)

Topik Riset: Information Retrieval System for Coastal Fisheries Marketplace (SITANPAS)

Pembimbing & Supervisor: Dr. Yuli Asmi Rahman & Pak Yusuf
