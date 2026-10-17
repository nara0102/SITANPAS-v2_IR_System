# src/tfidf_engine.py

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

class RetrievalEngine:
    def __init__(self, corpus_df, document_col, id_col):
        """
        Inisialisasi mesin pencarian dengan dataset korpus.
        
        Args:
            corpus_df (pd.DataFrame): DataFrame yang berisi dataset korpus.
            document_col (str): Nama kolom yang berisi teks fitur dokumen hasil preprocessing.
            id_col (str): Nama kolom yang berisi ID dokumen/produk unik.
        """
        self.corpus_df = corpus_df.copy()
        self.doc_col = document_col
        self.id_col = id_col
        self.corpus_texts = self.corpus_df[self.doc_col].fillna("").tolist()
        
        # --- INISIALISASI MESIN: TF-IDF & Cosine Similarity ---
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.corpus_texts)
        
        # --- INISIALISASI MESIN: CountVectorizer untuk Jaccard ---
        self.count_vectorizer = CountVectorizer(binary=True)
        self.count_matrix = self.count_vectorizer.fit_transform(self.corpus_texts)
        
        # --- INISIALISASI MESIN: BM25 ---
        tokenized_corpus = [doc.split() for doc in self.corpus_texts]
        self.bm25 = BM25Okapi(tokenized_corpus)

    # 1. METODE UTAMA: TF-IDF + Cosine Similarity
    def search_cosine(self, query_text):
        """Kalkulasi kemiripan menggunakan TF-IDF dan Cosine Similarity."""
        query_vec = self.tfidf_vectorizer.transform([query_text])
        cosine_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        return cosine_scores

    # 2. METODE PEMBANDING 1: Jaccard Similarity
    def search_jaccard(self, query_text):
        """Kalkulasi kemiripan menggunakan set intersection over union (Jaccard)."""
        query_vec = self.count_vectorizer.transform([query_text]).toarray()[0]
        count_array = self.count_matrix.toarray()
        
        jaccard_scores = []
        for doc_vec in count_array:
            intersection = np.logical_and(query_vec, doc_vec)
            union = np.logical_or(query_vec, doc_vec)
            score = intersection.sum() / float(union.sum()) if union.sum() > 0 else 0.0
            jaccard_scores.append(score)
            
        return np.array(jaccard_scores)

    # 3. METODE PEMBANDING 2: BM25
    def search_bm25(self, query_text):
        """Kalkulasi kemiripan menggunakan metode probabilitas pemeringkatan BM25."""
        tokenized_query = query_text.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        
        # BM25 menghasilkan skor absolute (bukan probabilitas 0-1), 
        # kita normalisasi min-max agar bisa dibandingkan sejajar dengan Cosine & Jaccard
        if len(bm25_scores) > 0 and bm25_scores.max() > 0:
            bm25_scores = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min())
        
        return np.array(bm25_scores)

    def retrieve(self, query_text, method='cosine', threshold=0.34, top_n=10):
        """
        Mengeksekusi pencarian dengan metode yang dipilih dan mengembalikan daftar produk relevan.
        
        Args:
            query_text (str): Teks kueri hasil preprocessing.
            method (str): 'cosine', 'jaccard', atau 'bm25'.
            threshold (float): Cut-off kelayakan skor (default 0.34 sesuai GEMINI_SKILL.md).
            top_n (int): Jumlah maksimal rekomendasi yang dikembalikan.
        """
        if method == 'cosine':
            scores = self.search_cosine(query_text)
        elif method == 'jaccard':
            scores = self.search_jaccard(query_text)
        elif method == 'bm25':
            scores = self.search_bm25(query_text)
        else:
            raise ValueError("Method must be 'cosine', 'jaccard', or 'bm25'")
            
        # Tambahkan skor ke salinan dataframe
        result_df = self.corpus_df.copy()
        result_df['relevance_score'] = scores
        result_df['method'] = method
        
        # Terapkan Threshold Filtering (Hanya ambil yang >= 0.34) dan Sorting Descending
        filtered_df = result_df[result_df['relevance_score'] >= threshold]
        sorted_df = filtered_df.sort_values(by='relevance_score', ascending=False)
        
        # Ambil Top-N dokumen
        final_df = sorted_df.head(top_n)
        
        # Kembalikan list of dict untuk ID produk dan skornya
        return final_df[[self.id_col, 'relevance_score', 'method']].to_dict('records')