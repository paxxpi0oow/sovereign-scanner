# 🛡️ Sovereign Security Scanner

> Offline network anomaly detection for Termux — async port scanner + pure NumPy autoencoder. No cloud, no TensorFlow, no telemetry.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Android-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Dependencies](https://img.shields.io/badge/dependencies-numpy%20only-brightgreen)

---

## 📖 Apa ini?

**Sovereign Security Scanner** adalah alat deteksi anomali jaringan yang berjalan **sepenuhnya offline** di Termux (Android). Alat ini memindai port pada host target, lalu menggunakan **autoencoder neural network** — ditulis dari nol menggunakan NumPy, tanpa TensorFlow atau PyTorch — untuk mendeteksi apakah pola port yang terbuka menyimpang dari "baseline normal" yang sudah dipelajari.

Cocok untuk:
- Pengguna Termux yang ingin **memantau keamanan jaringan lokal** tanpa mengirim data ke cloud.
- Pembelajar ML yang ingin melihat **bagaimana neural network bekerja dari dalam** (backpropagation manual, tanpa framework).
- Penggemar privasi yang tidak mau bergantung pada layanan pihak ketiga.

---

## ✨ Fitur

- ⚡ **Port scanner asinkron** — memindai 1024 port dalam hitungan detik menggunakan `asyncio`, bukan thread.
- 🧠 **Autoencoder murni NumPy** — backpropagation dan gradient descent ditulis manual. Tanpa framework berat.
- 🔒 **100% offline** — tidak ada telemetri, tidak ada API call, tidak ada cloud.
- 📱 **Ringan** — hanya butuh `numpy`. Jalan di HP kentang sekalipun.
- 🎯 **Deteksi berbasis baseline** — belajar pola normal dulu, baru tandai yang menyimpang.

---

## 🚀 Instalasi

### Prasyarat
- Termux (dari F-Droid, **bukan** dari Play Store — versi Play Store sudah usang)
- Koneksi internet (hanya untuk instalasi awal)

### Langkah-langkah

```bash
# 1. Clone repo
git clone https://github.com/paxxpi0oow/sovereign-scanner.git
cd sovereign-scanner

# 2. Jalankan installer otomatis
bash install.sh

# 3. Jalankan scanner
python main.py
```

**Instalasi manual** (kalau `install.sh` tidak bekerja):

```bash
pkg update && pkg upgrade -y
pkg install python python-numpy git -y
python main.py
```

---

## 🎮 Cara Pakai

```bash
python main.py
```

Kamu akan diminta memasukkan target:

```
Masukkan target untuk dipindai: 192.168.1.1
```

Program akan:

1. **Mengumpulkan baseline** — memindai `127.0.0.1` sebanyak 5 kali untuk mempelajari pola normal.
2. **Melatih model** — autoencoder belajar merekonstruksi pola baseline (1000 epoch, ±5 detik).
3. **Memindai target** — memeriksa port pada target yang kamu masukkan.
4. **Menilai anomali** — jika error rekonstruksi melebihi ambang batas (mean + 2σ), pola dianggap tidak normal.

### Contoh output

```
[*] Mengumpulkan baseline dari 127.0.0.1...
    Scan 1: 3 port terbuka
    Scan 2: 3 port terbuka
    Scan 3: 3 port terbuka
    Scan 4: 3 port terbuka
    Scan 5: 3 port terbuka
[*] Melatih neural network...
[*] Ambang batas anomali: 0.0012
[*] Memindai target: 192.168.1.1
[*] Open ports: [22, 80, 443]
[*] Reconstruction error: 0.0089
[!] ANOMALI TERDETEKSI: Pola port tidak seperti biasanya!
```

---

## 🧠 Bagaimana Cara Kerjanya?

### 1. Port Scanning (Asinkron)
`scanner.py` menggunakan `asyncio.open_connection` untuk membuka koneksi TCP secara paralel. `Semaphore` membatasi konkurensi agar tidak membanjiri jaringan atau kehabisan file descriptor.

### 2. Representasi Vektor
Hasil scan dikonversi menjadi **vektor biner 1024 dimensi** — setiap elemen bernilai `1` jika port terbuka, `0` jika tertutup.

### 3. Autoencoder
`neural_net.py` mengimplementasikan **autoencoder dengan satu hidden layer** (4 neuron):

```
Input (1024) → Hidden (4) → Output (1024)
```

Model dilatih hanya dengan data baseline (pola normal). Tujuannya: **merekonstruksi input seakurat mungkin**.

### 4. Deteksi Anomali
Saat memindai target baru:
- Jika pola **mirip baseline** → rekonstruksi bagus → error kecil → **normal** ✅
- Jika pola **berbeda jauh** → rekonstruksi buruk → error besar → **anomali** ⚠️

Ambang batas = `mean(train_errors) + 2 × std(train_errors)`. Ini heuristik sederhana yang bekerja baik untuk baseline yang stabil.

---

## 📁 Struktur Proyek

```
sovereign-scanner/
├── src/
│   ├── __init__.py       # Marker package Python
│   ├── scanner.py        # Port scanner asinkron (asyncio)
│   └── neural_net.py     # Autoencoder murni NumPy
├── main.py               # Entry point: gabungkan scanner + ML
├── install.sh            # Setup otomatis Termux
├── requirements.txt      # Dependensi (numpy)
├── README.md             # File ini
└── LICENSE               # MIT
```

---

## ⚠️ Batasan & Catatan

- **Bukan pengganti IDS profesional** — ini alat edukasi untuk memahami pola jaringan.
- **Baseline harus "bersih"** — kalau baseline dilatih saat jaringan sedang diserang, model akan menganggap serangan sebagai "normal".
- **Scan hanya host yang kamu miliki izinnya** — memindai jaringan tanpa izin adalah ilegal di banyak yurisdiksi.
- **Akurasi tergantung kualitas baseline** — jaringan yang sangat dinamis butuh lebih banyak sampel.

---

## 🛠️ Roadmap

- [ ] Mode `--save-model` dan `--load-model` (simpan model ke `.npz`)
- [ ] CLI dengan `argparse` untuk target ganda
- [ ] Dukungan UDP scan
- [ ] Export laporan ke JSON
- [ ] Antarmuka TUI menggunakan `rich`
- [ ] Unit test dengan `pytest`

Kontribusi sangat diterima! Silakan buka issue atau pull request.

---

## 📜 Lisensi

MIT License — lihat [LICENSE](LICENSE) untuk detail.

---

## ⚖️ Disclaimer

Alat ini disediakan **hanya untuk tujuan edukasi dan pengujian pada sistem milik sendiri**. Penggunaan terhadap sistem tanpa izin eksplisit adalah **ilegal** dan melanggar hukum. Penulis tidak bertanggung jawab atas penyalahgunaan.

---

## 🙏 Kredit

- Dibuat dengan ☕ dan 📱 di Termux
- Terinspirasi dari kebutuhan akan alat keamanan **offline-first** untuk Android
