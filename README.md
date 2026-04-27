# 🛒 E-Commerce Public Dataset — Proyek Analisis Data

Proyek analisis data menggunakan **Brazilian E-Commerce Public Dataset** dari Olist.  
Dashboard interaktif dibuat menggunakan **Streamlit**.

---

## 📁 Struktur Direktori

```
submission/
├── dashboard/
│   ├── main_data.csv         # Data utama untuk dashboard
│   ├── delivery_data.csv     # Data analisis pengiriman
│   ├── rfm_data.csv          # Data RFM segmentation
│   └── dashboard.py          # Aplikasi Streamlit
├── data/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── notebook.ipynb            # Notebook analisis data lengkap
├── requirements.txt          # Daftar library Python
└── README.md                 # File ini
```

---

## 🔍 Pertanyaan Bisnis

1. **Kategori produk apa yang menghasilkan total pendapatan tertinggi dan bagaimana tren penjualannya secara bulanan sepanjang periode 2017–2018?**

2. **Bagaimana distribusi waktu pengiriman rata-rata di setiap negara bagian (state) Brasil, dan state mana yang memiliki performa pengiriman terburuk?**

---

## 🚀 Cara Menjalankan Dashboard

### 1. Install Dependencies

Pastikan Python 3.8+ sudah terinstal.

```bash
pip install -r requirements.txt
```

### 2. Jalankan Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`

---

## 📦 Setup Environment (Opsional — dengan virtual environment)

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan (Windows)
venv\Scripts\activate

# Aktifkan (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Jalankan dashboard
cd dashboard
streamlit run dashboard.py
```

---

## 📊 Fitur Dashboard

- **Filter Periode**: Pilih rentang tanggal analisis secara interaktif
- **KPI Metrics**: Total revenue, orders, avg order value, avg review score
- **Tab 1 — Kategori & Revenue**: Top N kategori produk + tren revenue bulanan
- **Tab 2 — Pengiriman**: Performa pengiriman per state + distribusi delivery days
- **Tab 3 — RFM Segmentation**: Segmentasi pelanggan berdasarkan Recency, Frequency, Monetary

---

## 🛠️ Tech Stack

- Python 3.8+
- Pandas, NumPy
- Matplotlib, Seaborn
- Streamlit
