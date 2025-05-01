[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=900&size=25&pause=1000&color=56F7F0&background=FB16EE00&width=440&lines=PHISPYRATE+Face+Verification)](https://git.io/typing-svg)

# PHISPYRATE_FaceVerification

Simulasi verifikasi wajah Android berbasis web untuk keperluan edukasi, OSINT, atau penetration testing. Tool ini menampilkan antarmuka mirip autentikasi wajah Android dan dapat dijalankan secara lokal atau melalui tunneling seperti **Ngrok** atau **LocalXpose**.

---

### 📸 Tampilan Tools

![PHISPYRATE Screenshot] (https://imgur.com/a/phispyrate-4Ha2W5Z)

---

## 📁 Struktur Folder
```
PHISPYRATE_FaceVerification/
├── server.py                    ← Backend Flask utama
├── requirements.txt             ← Daftar dependensi Python
├── ngrok, loclx                 ← Binary tunneling tools
├── ngrok_token.txt              ← Token untuk Ngrok
├── localxpose_token.txt         ← Token untuk LocalXpose
├── ngrok_url.txt, fake_url.txt  ← Output URL publik
├── static/
│   ├── android_logo.png         ← Logo Android
│   ├── script.js                ← Script kamera & upload
│   ├── sound.mp3                ← Efek suara saat verifikasi
│   └── style.css                ← Styling tampilan UI
├── templates/
│   └── index.html               ← Tampilan halaman utama
├── uploads/
│   └── hasil.txt                ← Simpan hasil upload
```

## ✨ Fitur Utama
- Simulasi otentikasi wajah dengan UI seperti Android
- Kamera langsung aktif dengan deteksi area wajah
- Rekam video otomatis dan kirim ke server
- Verifikasi acak (berhasil/gagal) + efek suara
- Mendukung tunneling via **Ngrok** & **LocalXpose**
- Hasil URL ditampilkan dan disimpan otomatis

## ⚙️ Instalasi

1. Clone repositori:
```bash
git clone https://github.com/rivaile96/PHISPYRATE_FaceVerification.git
cd PHISPYRATE_FaceVerification
```

2. (Opsional) Buat virtual environment:
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

3. Install dependensi:
```bash
pip install -r requirements.txt
```

## 🚀 Menjalankan Aplikasi

```bash
python server.py
```

Lalu pilih salah satu mode:
- `1`: Ngrok (recommended, pastikan punya token)
- `2`: LocalXpose (pastikan punya token)
- `3`: Jalankan lokal (`http://localhost:5000`)

URL publik akan tampil di terminal dan disimpan ke file `.txt`.

## 📦 Contoh File `.gitignore`
```
venv/
__pycache__/
*.pyc
uploads/
*.txt
ngrok
loclx
```

## ⚠️ Disclaimer
Proyek ini hanya untuk pembelajaran dan riset keamanan. Segala bentuk penyalahgunaan adalah tanggung jawab pengguna. Gunakan hanya dengan persetujuan dari pihak terkait.

## 📄 Lisensi
MIT License  
Created by **Rivaile** – 2025
