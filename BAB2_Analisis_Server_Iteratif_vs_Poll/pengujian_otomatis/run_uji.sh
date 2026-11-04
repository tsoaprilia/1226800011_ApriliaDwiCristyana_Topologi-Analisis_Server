#!/bin/bash
# run_uji.sh - kompilasi, rekam (tcpdump), jalankan server dan klien penguji.
# Dijalankan sebagai root (untuk tcpdump):  sudo bash run_uji.sh [skenario...]
# Server dan klien dijalankan sebagai pengguna biasa.
set -u
U=${SUDO_USER:-windows}                       # pengguna biasa untuk server & klien
DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$DIR/../src"
OUT="$DIR/hasil"
KLIEN="$DIR/uji_klien.py"
B=/home/$U/uji_build
PORT=5000

mkdir -p "$OUT" && runuser -u $U -- mkdir -p "$B"
cp "$SRC/s1_server_iteratif.c" "$SRC/s2_server_poll.c" "$B/" && chown $U "$B"/*.c
cd "$B"
{
  echo "\$ gcc -Wall -Wextra -O2 -o s1_server s1_server_iteratif.c"
  runuser -u $U -- gcc -Wall -Wextra -O2 -o s1_server s1_server_iteratif.c 2>&1
  echo "\$ gcc -Wall -Wextra -O2 -o s2_server s2_server_poll.c"
  runuser -u $U -- gcc -Wall -Wextra -O2 -o s2_server s2_server_poll.c 2>&1
  echo "exit=$?  ($(gcc --version | head -1))"
} > "$OUT/kompilasi.txt"

ss_snap() {   # $1 = jeda, $2 = berkas
  ( sleep "$1"
    { echo "# ss -ltn  (baris LISTEN: Recv-Q = koneksi antre belum di-accept)"; ss -ltn "sport = :$PORT"
      echo; echo "# ss -tn  (Recv-Q = byte belum dibaca aplikasi, Send-Q = byte belum di-ACK peer)"
      ss -tn "( sport = :$PORT )"; } > "$2" ) &
}

jalankan() {  # $1 = binari server, $2 = skenario, $3 = snaplen
  local srv=$1 sk=$2 snap=${3:-0}
  echo "=== $sk ==="
  tcpdump -i lo -U -nn -s "$snap" -w "$OUT/$sk.pcap" "tcp port $PORT" 2>/dev/null &
  local tp=$!
  sleep 1
  runuser -u $U -- stdbuf -oL ./$srv $PORT > "$OUT/$sk.server.log" 2>&1 &
  sleep 0.5
  case $sk in
    s1-dua)     ss_snap 1.6 "$OUT/$sk.ss.txt" ;;
    s1-banjir)  ss_snap 2.5 "$OUT/$sk.ss.txt" ;;
    s1-backlog) ss_snap 3.0 "$OUT/$sk.ss.txt" ;;
    s2-lambat)  ss_snap 9.0 "$OUT/$sk.ss.txt" ;;
  esac
  runuser -u $U -- python3 -I "$KLIEN" "$sk" --port $PORT > "$OUT/$sk.klien.log" 2>&1
  sleep 1.5
  pkill -x $srv; sleep 0.3
  kill -INT $tp; wait $tp 2>/dev/null
  echo "   pcap: $(stat -c %s "$OUT/$sk.pcap") byte"
}

DAFTAR=${*:-"s1-dua s1-pecah s1-banjir s1-backlog s2-chat s2-nama s2-pecah s2-gabung s2-panjang s2-penuh s2-lambat"}
for sk in $DAFTAR; do
  case $sk in
    s1-banjir) jalankan s1_server $sk 200 ;;
    s1-*)      jalankan s1_server $sk ;;
    s2-lambat) jalankan s2_server $sk 200 ;;
    s2-*)      jalankan s2_server $sk ;;
  esac
done
chown -R $U "$OUT" 2>/dev/null
echo SELESAI
