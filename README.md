
# **Irrigation CSP Solver**

Program ini dibuat buat **menyelesaikan penjadwalan irigasi** menggunakan **CSP (Constraint Satisfaction Problem)** dengan kombinasi **Backtracking**, **MRV heuristic**, dan **Forward Checking**. Dataset dibuat otomatis saat program dijalankan.

---

## 📁 **Struktur File Otomatis**

Saat program dijalankan, script akan otomatis generate dua file:

| File                           | Fungsi                                 |
| ------------------------------ | -------------------------------------- |
| `dataset_irigasi_50_petak.csv` | Dataset lengkap petak sawah + provinsi |
| `data_csp_irigasi.csv`         | Dataset yang dirapikan untuk CSP       |

---

## **Apa yang Dilakukan Program Ini?**

Secara singkat:

1. Generate dataset acak 50 petak sawah.
2. Setup model CSP:

   * **Variabel:** nama kabupaten
   * **Domain:** Hari_1 — Hari_7
3. Terapkan constraint:

   * Petak dalam provinsi yang sama **nggak boleh di hari yang sama**
   * Kapasitas jam harian dicek
   * Prioritas tinggi harus dapat hari lebih awal
4. Jalankan eksperimen dengan algoritma:

   * **Backtracking + MRV**
   * **Backtracking + MRV + Forward Checking**
5. Tampilkan performa algoritma dan **visualisasi heatmap hasil optimal**.

---

##  **Cara Menjalankan Program**

Pastikan sudah install Python 3 dan library dependency.

### 1️⃣ Install dependencies

```sh
pip install pandas numpy matplotlib seaborn
```

### 2️⃣ Jalankan program

```sh
python irrigation_csp.py
```

---

## 📊 Output yang Akan Ditampilkan

| Output                     | Isi                                     |
| -------------------------- | --------------------------------------- |
| Tabel performa algoritma   | Berapa lama search, berhasil/tidak      |
| Heatmap visualisasi solusi | Jadwal irigasi dalam bentuk tabel warna |
| File CSV dataset           | Bisa dicek manual                       |

Contoh tampilan terminal:

```
Running: BT + MRV...
Running: BT + MRV + FC...

=== HASIL EKSPERIMEN ===
Algoritma         Waktu (s)   Status     Terjadwal
BT + MRV          2.8711      Gagal      35/50
BT + MRV + FC     0.5518      Berhasil   50/50
```

---

## ❗ Catatan Singkat

* Jangan lupa install library dulu.
* Program otomatis jalan hingga visualisasi muncul.
* Kalau nggak ada solusi valid, heatmap nggak ditampilkan.

---
