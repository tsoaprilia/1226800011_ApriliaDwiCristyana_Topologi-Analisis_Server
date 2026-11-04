# BAB 2 – Analisis Server Iteratif dan Server Berbasis `poll()`

Menguji `s1_server_iteratif.c` (S1, server echo iteratif) dan `s2_server_poll.c` (S2, server chat multi-pengguna dengan `poll()`) di Wireshark, lalu membandingkan source code keduanya. Laporan lengkap ada di [`../laporan/Laporan Praktikum Jaringan - BAB 1-3.docx`](../laporan/) (BAB 2).

## Isi folder

```
BAB2_Analisis_Server_Iteratif_vs_Poll/
├── src/
│   ├── s1_server_iteratif.c     ← S1: accept → recv/send sampai klien keluar → accept berikutnya
│   └── s2_server_poll.c         ← S2: satu thread, poll() memantau listener + hingga 32 klien
├── capture_manual/
│   ├── s1_iteratif.pcap         ← uji manual S1 dengan 2 klien Netcat
│   └── s2_poll.pcap             ← uji manual S2: registrasi, chat, /who, /quit
└── pengujian_otomatis/
    ├── uji_klien.py             ← klien penguji Python (11 skenario, pustaka standar)
    ├── run_uji.sh               ← kompilasi + tcpdump + jalankan server & klien
    ├── hasil/                   ← per skenario: .pcap, .server.log, .klien.log, .ss.txt
    ├── screenshot/              ← 01–15 Wireshark, T01–T09 keluaran terminal
    └── term/                    ← perintah yang menghasilkan screenshot T01–T09
```

## Kompilasi dan menjalankan

```bash
gcc -Wall -Wextra -O2 -o s1_server src/s1_server_iteratif.c
gcc -Wall -Wextra -O2 -o s2_server src/s2_server_poll.c
./s1_server 5000          # atau ./s2_server 5000
nc 127.0.0.1 5000         # klien manual
```

Keduanya listen di `127.0.0.1:5000`, jadi capture harus diambil di interface loopback Linux/WSL:

```bash
sudo tcpdump -i lo -nn -s 0 -w hasil.pcap "tcp port 5000"
```

Pengujian otomatis semua skenario (Linux/WSL, butuh `gcc`, `tcpdump`, `python3`, `ss`):

```bash
cd pengujian_otomatis
sudo bash run_uji.sh                    # semua skenario
sudo bash run_uji.sh s1-banjir s2-lambat  # skenario tertentu
```

## Skenario pengujian otomatis

| Skenario | Server | Yang diuji | Hasil utama |
|---|---|---|---|
| `s1-dua` | S1 | Klien B mengirim saat A masih aktif | Echo B tertunda 3,02 s; `ss`: B antre di accept queue, Recv-Q 12 byte |
| `s1-pecah` | S1 | 1 baris dikirim dalam 3 segmen | S1 memantulkan 3 potongan terpisah (tanpa framing) |
| `s1-banjir` | S1 | A diam, B mengirim 64 KB terus | 34 TCP ZeroWindow, B macet 4,78 s |
| `s1-backlog` | S1 | 25 koneksi saat S1 sibuk | Antrean penuh di 17 koneksi, 8 klien gagal, 48 SYN diulang |
| `s2-chat` | S2 | 3 pengguna + 1 klien diam | Broadcast 1 → N-1 dalam ~1 ms; klien diam tidak menghambat |
| `s2-nama` | S2 | Nama berspasi, terlalu panjang, ganda | Ditolak dengan `!!!` lalu FIN dari server |
| `s2-pecah` | S2 | 1 baris dalam 3 segmen | Digabung menjadi 1 pesan setelah `\n` tiba |
| `s2-gabung` | S2 | 3 baris dalam 1 segmen | Dipecah menjadi 3 pesan, CR dibuang |
| `s2-panjang` | S2 | 2100 byte tanpa newline | `!!! baris terlalu panjang` lalu RST |
| `s2-penuh` | S2 | 33 koneksi serentak | Koneksi ke-33 menerima `!!! server penuh` |
| `s2-lambat` | S2 | 1 klien tidak pernah membaca | `send()` blocking membekukan seluruh server 5,2 s |

## Kesimpulan singkat

- **S1** hanya melayani satu klien pada satu waktu karena terjebak di loop `recv()` milik klien aktif. Kernel tetap menyelesaikan handshake dan meng-ACK data klien lain, tetapi aplikasi baru memprosesnya setelah klien pertama keluar.
- **S2** melayani banyak klien dalam satu thread dengan `poll()`, memiliki buffer dan framing baris per klien, validasi nama, serta batas 32 klien. Kelemahannya: `send()` masih blocking, sehingga satu klien yang tidak membaca dapat membekukan semua pengguna.

## Catatan

- `run_uji.sh` memakai path relatif terhadap lokasi skrip. Server dan klien dijalankan sebagai `$SUDO_USER`.
- Pada `s1-banjir` dan `s2-lambat`, tcpdump memakai snaplen 200 byte agar file kecil; header TCP tetap utuh.
- Screenshot `T01`–`T09` adalah keluaran terminal asli dari WSL yang dirender menjadi gambar; perintahnya ada di folder `term/`.
