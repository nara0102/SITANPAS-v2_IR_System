# src/preprocessing.py
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class SitanpasPreprocessor:
    def __init__(self):
        # Inisialisasi Sastrawi (karena berat, cukup dilakukan sekali saat objek dibuat)
        self.stemmer = StemmerFactory().create_stemmer()
        
        # Ambil stopwords bawaan Sastrawi
        factory = StopWordRemoverFactory()
        self.base_stopwords = factory.get_stop_words()
        
        # TODO: KALIBRASI STOPWORDS (Sesuai aturan GEMINI_SKILL.md Iterasi Evaluasi)
        # Tambahkan kata-kata umum e-commerce pesisir yang tidak bermakna di sini
        self.custom_stopwords = [
            'jual', 'beli', 'harga', 'murah', 'segar', 'ready', 'stok', 'promo',
            'ikan', 'laut', 'hasil', 'tangkapan', 'nelayan', 'ambesia', 'selatan' 
        ]
        
        self.all_stopwords = set(self.base_stopwords + self.custom_stopwords)

    def preprocess(self, text):
        if not isinstance(text, str):
            return ""
            
        # 1. Case Folding & Basic Cleaning (Hanya ambil huruf dan angka)
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # 2. Tokenization & 3. Filtering (Sekaligus)
        tokens = text.split()
        filtered_tokens = [word for word in tokens if word not in self.all_stopwords]
        
        # 4. Stemming (Sastrawi)
        stemmed_text = " ".join(filtered_tokens)
        final_text = self.stemmer.stem(stemmed_text)
        
        return final_text

    def create_document_feature(self, row):
        """
        Aturan Feature Combining: D_j = nama_produk + " " + kategori + " " + deskripsi
        """
        nama = str(row.get('nama_produk', ''))
        kategori = str(row.get('kategori', ''))
        deskripsi = str(row.get('deskripsi', ''))
        
        combined_text = f"{nama} {kategori} {deskripsi}"
        return self.preprocess(combined_text)