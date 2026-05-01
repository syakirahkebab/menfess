# BOT MENFESS (Python 3.11)

Bot menfess Telegram berbasis **Pyrogram** dengan MongoDB.
Konfigurasi sekarang terpusat di file **`.env`** agar stabil saat deploy ke VPS.

## 1) Persiapan VPS (Ubuntu)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip git
```

## 2) Clone project

```bash
git clone https://github.com/nekolocal/nekomenfess menfess
cd menfess
```

## 3) Buat virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 4) Konfigurasi `.env`

```bash
cp .env.example .env
nano .env
```

Wajib diisi dengan benar:
- `API_ID`, `API_HASH`, `BOT_TOKEN`
- `DB_URL`, `DB_NAME`
- `CHANNEL_1`, `CHANNEL_2`, `CHANNEL_LOG`
- `ID_ADMIN`

Catatan penting:
- Semua `CHANNEL_*` harus ID channel/supergroup valid (format `-100...`).
- Bot wajib sudah masuk channel dan memiliki izin admin yang diperlukan.
- Jadwal reset harian bisa diatur lewat:
  - `RESET_TIMEZONE` (contoh: `Asia/Jakarta`)
  - `RESET_HOUR`, `RESET_MINUTE`

## 5) Jalankan bot

```bash
python3.11 main.py
```

## 6) Jalankan dengan systemd (direkomendasikan)

Buat service:

```bash
sudo nano /etc/systemd/system/menfess.service
```

Isi contoh:

```ini
[Unit]
Description=Menfess Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/menfess
EnvironmentFile=/path/to/menfess/.env
ExecStart=/path/to/menfess/.venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Aktifkan:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now menfess
sudo systemctl status menfess
```

## Troubleshooting singkat

- **Database sering tidak terbaca**
  - Pastikan `DB_URL` valid dan whitelist IP VPS di MongoDB Atlas.
  - Pastikan DNS VPS normal (`nslookup cluster...mongodb.net`).
- **Channel tidak terbaca**
  - Cek ID channel benar.
  - Cek bot sudah admin di channel/channel log.
- **Bot tidak start**
  - Jalankan manual dulu `python3.11 main.py` untuk lihat error awal.

