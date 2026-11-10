#!/data/data/com.termux/files/usr/bin/bash
set -e
pkg update -y && pkg upgrade -y
pkg install python python-numpy git -y
echo "[+] Dependensi terpasang. Jalankan: python main.py"
