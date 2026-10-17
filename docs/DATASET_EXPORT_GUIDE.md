# 📊 Guide Export Dataset & Skema Database — SITANPAS IR System

Dokumen ini berfungsi sebagai panduan operasional untuk mengekstrak (*export*) *ground truth dataset* dari database Supabase SITANPAS v2 ke dalam format CSV. Dataset ini digunakan sebagai masukan (*input corpus*) pada pipeline **Information Retrieval (IR)** berbasis algoritma **TF-IDF** dan **Cosine Similarity**.

---

## 🎯 1. Alur Export Dataset (Ground Truth)

Setiap kali terjadi penambahan atau pembaruan data produk ikan di database Supabase, ikuti langkah berikut untuk memperbarui dataset lokal:

1. Buka **Supabase Dashboard** $\rightarrow$ pilih proyek **SITANPAS**.
2. Masuk ke menu **SQL Editor** pada *sidebar* sebelah kiri.
3. Tempelkan (*paste*) *query* SQL khusus IR di bawah ini.
4. Klik tombol **Run** (atau tekan `Cmd + Enter`).
5. Pada bagian **Query Result**, klik **Export CSV** $\rightarrow$ simpan file dengan nama `sitanpas_dataset_raw.csv` di folder `data/` proyek IR milikmu.

---

## 🔍 2. Query SQL Teroptimasi untuk Feature Extraction

Query ini menggabungkan data produk dengan informasi profil nelayan/penjual, serta menyaring produk yang aktif agar siap digunakan dalam pemprosesan teks (*text preprocessing*).

```sql
SELECT 
    p.id AS product_id,
    p.nama_produk,
    p.kategori,
    COALESCE(p.deskripsi, '') AS deskripsi,
    p.harga,
    p.stok,
    p.unit_type AS satuan,
    p.berat_per_unit AS berat_kg,
    COALESCE(u.nama_lengkap, u.full_name, u.email) AS nama_nelayan,
    COALESCE(u.address, 'Palu') AS lokasi_nelayan,
    p.status,
    p.created_at
FROM public.products p
LEFT JOIN public.users u ON p.nelayan_id = u.id
WHERE p.status = 'active' AND p.stok > 0
ORDER BY p.created_at DESC;
```
