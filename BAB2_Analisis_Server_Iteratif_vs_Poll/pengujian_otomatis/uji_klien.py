#!/usr/bin/env python3
"""uji_klien.py - klien penguji untuk s1_server_iteratif.c (S1) dan s2_server_poll.c (S2).
Hanya memakai pustaka standar Python. Jalankan sambil merekam (tcpdump -i lo tcp port 5000).

  S1 (server iteratif, echo)
    s1-dua      dua klien serentak, B mengirim saat A masih aktif
    s1-pecah    satu baris dikirim dalam 3 segmen -> S1 memantulkan 3 potongan
    s1-banjir   A diam, B mengirim 64 KB terus-menerus (TCP ZeroWindow)
    s1-backlog  A menahan server, 25 koneksi baru serentak (SYN diulang)
  S2 (server chat poll)
    s2-chat     klien 'diam' (tidak kirim nama) + budi, sari, andi: chat, /who, /quit
    s2-nama     nama tidak valid dan nama ganda
    s2-pecah    satu baris dalam 3 segmen -> digabung jadi 1 baris
    s2-gabung   tiga baris dalam 1 segmen -> dipecah jadi 3 pesan
    s2-panjang  baris > 2048 byte tanpa newline -> "baris terlalu panjang"
    s2-penuh    33 koneksi serentak (batas MAKS_KLIEN = 32)
    s2-lambat   satu klien tidak pernah membaca -> send() blocking membekukan server
Opsi: --host 127.0.0.1 --port 5000
"""
import argparse
import socket
import sys
import threading
import time

T0 = time.time()


def log(tag, msg):
    print(f"{time.time() - T0:7.3f}s [{tag}] {msg}", flush=True)


def sambung(h, p, tag, rcvbuf=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if rcvbuf:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, rcvbuf)
    s.settimeout(5)
    s.connect((h, p))
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    log(tag, f"terhubung dari port lokal {s.getsockname()[1]}")
    return s


def baca(s, tag, tunggu=0.5, tampil=True):
    s.settimeout(tunggu)
    data = b""
    try:
        while True:
            b = s.recv(65536)
            if not b:
                break
            data += b
    except (socket.timeout, BlockingIOError):
        pass
    except ConnectionError as e:
        log(tag, f"<< koneksi error: {e}")
    if tampil:
        if data:
            for baris in data.decode(errors="replace").splitlines():
                log(tag, f"<< {baris[:90]}{'...' if len(baris) > 90 else ''}")
        else:
            log(tag, "<< (tidak ada balasan)")
    return data


def kirim(s, tag, teks):
    tampil = teks if len(teks) <= 60 else teks[:40] + f"... ({len(teks)} byte)"
    log(tag, f">> {tampil!r}")
    s.sendall(teks.encode())


def daftar(h, p, nama, rcvbuf=None):
    s = sambung(h, p, nama, rcvbuf)
    baca(s, nama)
    kirim(s, nama, nama + "\n")
    baca(s, nama)
    return s

# ------------------------------------------------------------------ S1


def s1_dua(h, p):
    a = sambung(h, p, "A")
    kirim(a, "A", "halo dari A\n"); baca(a, "A")
    b = sambung(h, p, "B")
    t_kirim = time.time()
    kirim(b, "B", "halo dari B\n"); baca(b, "B", 2.5)
    kirim(a, "A", "A masih di sini\n"); baca(a, "A")
    log("A", "menutup koneksi (FIN)"); a.close()
    baca(b, "B", 1.0)
    log("B", f"echo B diterima +{time.time() - t_kirim:.3f}s setelah dikirim")
    b.close()


def s1_pecah(h, p):
    a = sambung(h, p, "A")
    for potong in ["sel", "amat pa", "gi\n"]:
        kirim(a, "A", potong); baca(a, "A", 0.5)
    a.close()


def s1_banjir(h, p):
    a = sambung(h, p, "A")
    b = sambung(h, p, "B")
    b.setblocking(False)
    total, blok, t0 = 0, b"X" * 65536, time.time()
    while time.time() - t0 < 5:
        try:
            total += b.send(blok)
        except BlockingIOError:
            time.sleep(0.1)
    log("B", f"berhasil menitip {total} byte ke kernel sebelum macet (lihat TCP ZeroWindow)")
    log("A", "menutup koneksi"); a.close()
    time.sleep(1); b.close()


def s1_backlog(h, p, n=25):
    a = sambung(h, p, "A")
    soket = []
    for _ in range(n):
        s = socket.socket(); s.setblocking(False)
        s.connect_ex((h, p)); soket.append(s)
    log("main", f"{n} SYN dikirim; tunggu 8 detik")
    time.sleep(8)
    for s in soket:
        s.close()
    a.close()

# ------------------------------------------------------------------ S2


def s2_chat(h, p):
    diam = sambung(h, p, "diam")            # tersambung tetapi tidak pernah mengirim nama
    baca(diam, "diam")
    budi = daftar(h, p, "budi")
    sari = daftar(h, p, "sari"); baca(budi, "budi")
    andi = daftar(h, p, "andi"); baca(budi, "budi"); baca(sari, "sari")
    kirim(budi, "budi", "halo semua\n")
    baca(sari, "sari"); baca(andi, "andi"); baca(budi, "budi"); baca(diam, "diam")
    kirim(sari, "sari", "/who\n"); baca(sari, "sari")
    kirim(andi, "andi", "/quit\n"); baca(andi, "andi")
    baca(budi, "budi"); baca(sari, "sari")
    budi.close(); baca(sari, "sari")
    sari.close(); diam.close()


def s2_nama(h, p):
    s = sambung(h, p, "x1"); baca(s, "x1")
    kirim(s, "x1", "nama spasi!\n"); baca(s, "x1"); s.close()
    s = sambung(h, p, "x2"); baca(s, "x2")
    kirim(s, "x2", "nama_yang_terlalu_panjang\n"); baca(s, "x2"); s.close()
    r = daftar(h, p, "rina")
    s = sambung(h, p, "x3"); baca(s, "x3")
    kirim(s, "x3", "rina\n"); baca(s, "x3"); s.close()
    r.close()


def s2_pecah(h, p):
    a = daftar(h, p, "penerima")
    b = daftar(h, p, "pengirim"); baca(a, "penerima")
    for potong in ["sel", "amat pa", "gi\n"]:
        kirim(b, "pengirim", potong); time.sleep(0.5)
    baca(a, "penerima")
    a.close(); b.close()


def s2_gabung(h, p):
    a = daftar(h, p, "penerima")
    b = daftar(h, p, "pengirim"); baca(a, "penerima")
    kirim(b, "pengirim", "satu\r\ndua\ntiga\n")    # 3 baris, 1 send, termasuk CRLF
    baca(a, "penerima")
    a.close(); b.close()


def s2_panjang(h, p):
    a = daftar(h, p, "saksi")
    b = daftar(h, p, "panjang"); baca(a, "saksi")
    kirim(b, "panjang", "A" * 2100)               # tanpa '\n'
    baca(b, "panjang", 1.0); baca(a, "saksi")
    b.close(); a.close()


def s2_penuh(h, p, n=33):
    soket = [sambung(h, p, f"k{i:02d}") for i in range(n)]
    baca(soket[-1], f"k{n - 1:02d}", 1.0)
    for s in soket:
        s.close()


def s2_lambat(h, p, durasi=6.0):
    korban = daftar(h, p, "korban")
    lambat = daftar(h, p, "lambat", rcvbuf=4096)  # setelah ini TIDAK PERNAH membaca
    pengirim = daftar(h, p, "pengirim")
    baca(korban, "korban"); baca(lambat, "lambat")

    status = {"byte": 0, "terakhir": None, "henti": False}

    def pembaca():
        korban.settimeout(0.2)
        while not status["henti"]:
            try:
                b = korban.recv(65536)
                if not b:
                    break
                status["byte"] += len(b); status["terakhir"] = time.time()
            except socket.timeout:
                pass
            except OSError:
                break
    th = threading.Thread(target=pembaca, daemon=True); th.start()

    pengirim.setblocking(False)
    baris = ("x" * 1500 + "\n").encode()
    dikirim, t0, baru, t_baru = 0, time.time(), None, None
    log("pengirim", "mulai banjir baris 1501 byte")
    while time.time() - t0 < durasi:
        try:
            pengirim.send(baris); dikirim += 1
        except BlockingIOError:
            time.sleep(0.05)
        if baru is None and time.time() - t0 > 3.0:
            log("korban", f"menerima {status['byte']} byte; terakhir pada "
                f"{(status['terakhir'] or T0) - T0:.3f}s")
            baru = socket.socket(); baru.settimeout(5)
            baru.connect((h, p)); t_baru = time.time()
            log("baru", f"terhubung (handshake sukses) dari port {baru.getsockname()[1]}; menunggu prompt...")
            baca(baru, "baru", 1.5)
    log("pengirim", f"{dikirim} baris dititipkan ke kernel")
    log("korban", f"total diterima {status['byte']} byte; terakhir pada {(status['terakhir'] or T0) - T0:.3f}s")
    log("lambat", "menutup koneksi tanpa membaca (RST)")
    lambat.close()
    data = baca(baru, "baru", 1.5, tampil=False)
    log("baru", f"prompt diterima +{time.time() - t_baru:.3f}s setelah handshake: {data[:40]!r}")
    time.sleep(1.0)
    log("korban", f"setelah lambat keluar total diterima {status['byte']} byte")
    status["henti"] = True
    for s in (pengirim, korban, baru):
        s.close()


SKENARIO = {
    "s1-dua": s1_dua, "s1-pecah": s1_pecah, "s1-banjir": s1_banjir, "s1-backlog": s1_backlog,
    "s2-chat": s2_chat, "s2-nama": s2_nama, "s2-pecah": s2_pecah, "s2-gabung": s2_gabung,
    "s2-panjang": s2_panjang, "s2-penuh": s2_penuh, "s2-lambat": s2_lambat,
}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("skenario", choices=SKENARIO)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5000)
    arg = ap.parse_args()
    try:
        SKENARIO[arg.skenario](arg.host, arg.port)
    except ConnectionError as e:
        log("main", f"koneksi gagal: {e}"); sys.exit(1)
