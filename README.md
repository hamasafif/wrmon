# 📊 wrmon - Terminal Storage & Network Monitor

**wrmon** adalah aplikasi monitoring ringan berbasis terminal (TUI) yang menampilkan informasi real-time tentang storage dan lalu lintas jaringan (upload/download speed), terinspirasi oleh tampilan visual seperti **btop**.

![textual](https://img.shields.io/badge/Textual-UI-green?logo=python&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)
![Platform](https://img.shields.io/badge/Linux-Windows-orange?logo=linux)

---

## 🚀 Fitur Utama

- 🧮 Menampilkan informasi disk usage (Total, Used, Free)
- 🌐 Monitoring upload & download speed secara real-time
- 💡 Tampilan TUI modern dengan Textual
- 🧰 Dibuat dengan `psutil` dan `textual` (100% Python)

---

## 🖼️ Screenshot

*(Tambahkan tangkapan layar di sini jika ada)*  
Contoh tampilan:
┌──────────────────────────────┐
│ wrmon Monitor │
├───────────────┬──────────────┤
│ Storage Info │ Network │
├───────────────┼──────────────┤
│ /dev/sda1 │ ↑ 2.31 MB/s │
│ Total: 480GB │ ↓ 5.42 MB/s │
│ Used : 302GB │ │
│ Free : 178GB │ │
└───────────────┴──────────────┘


---

## ⚙️ Instalasi

### 1. Clone repo ini

```bash
git clone https://github.com/NamaUser/wrmon.git
cd wrmon
pip install -r requirements.txt
pip install psutil textual

---


---

### 1. Menjalankan Aplikasi

```bash
textual run wrmon.py
Atau buat environment di /usr/local/bin
```
---

🧼 TODO & Fitur Mendatang
 Pilihan untuk interface jaringan tertentu

 Export data ke file log atau CSV

 Tampilan grafik sederhana (jika memungkinkan)

🧑‍💻 Kontribusi
Pull request dan masukan sangat terbuka!
Silakan fork repository ini dan kirimkan PR.

📄 Lisensi
Proyek ini dirilis di bawah lisensi MIT.
Lihat LICENSE untuk informasi lebih lanjut.

Dibuat dengan ❤️ oleh wrjunior



