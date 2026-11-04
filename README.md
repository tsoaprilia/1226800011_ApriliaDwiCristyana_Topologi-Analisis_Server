# Topologi & Analisis Server

Kumpulan tugas praktikum Jaringan Komputer (S2): simulasi routing di Cisco Packet Tracer dan analisis dua server TCP berbahasa C dengan Wireshark.

| BAB | Topik | Folder | Alat |
|---|---|---|---|
| 1 | Mengganti static routing dengan RIP v2 (dynamic routing) | [`BAB1_RIP_Dynamic_Routing`](BAB1_RIP_Dynamic_Routing/) | Cisco Packet Tracer 9.0.1 |
| 2 | Perbandingan server iteratif dan server multiplexing `poll()` | [`BAB2_Analisis_Server_Iteratif_vs_Poll`](BAB2_Analisis_Server_Iteratif_vs_Poll/) | C (gcc), WSL Ubuntu, tcpdump, Wireshark |
| 3 | Fungsi default gateway pada topologi papan tulis (static routing) | [`BAB3_Default_Gateway_Static_Routing`](BAB3_Default_Gateway_Static_Routing/) | Cisco Packet Tracer 9.0.1 |

## Struktur folder

```
TOPOLOGI & ANALISIS SERVER/
├── README.md                          ← file ini
├── laporan/
│   └── Laporan Praktikum Jaringan - BAB 1-3.docx   ← laporan lengkap BAB 1, 2, 3 (Times New Roman 10, spasi 1)
├── BAB1_RIP_Dynamic_Routing/
│   ├── README.md
│   ├── RIP_Dynamic_Routing_v2.pkt     ← file Packet Tracer
│   ├── konfigurasi/                   ← running-config Router0 & Router1 (teks)
│   └── screenshot/                    ← 15 gambar bukti (01–15)
├── BAB2_Analisis_Server_Iteratif_vs_Poll/
│   ├── README.md
│   ├── src/                           ← s1_server_iteratif.c, s2_server_poll.c
│   ├── capture_manual/                ← capture uji manual dengan Netcat
│   └── pengujian_otomatis/            ← klien penguji, skrip, 11 capture, log, screenshot
└── BAB3_Default_Gateway_Static_Routing/
    ├── README.md
    ├── Static_Routing_Default_Gateway_v3.pkt
    ├── konfigurasi/                   ← running-config R0 & R1 (teks)
    └── screenshot/                    ← 22 gambar bukti (01–22)
```

## Cara membuka

- **`.pkt`**: buka dengan Cisco Packet Tracer 9.0.1 atau versi lebih baru. Tunggu sekitar 30 detik sampai semua lampu link hijau sebelum menguji.
- **`.pcap`**: buka dengan Wireshark (File → Open). Filter dasar: `tcp.port == 5000`.
- **`laporan/Laporan Praktikum Jaringan - BAB 1-3.docx`**: satu laporan gabungan berisi analisis, tabel, dan screenshot untuk ketiga BAB.
- **`konfigurasi/*.txt`**: running-config router hasil ekstraksi dari file `.pkt`, dapat dibaca langsung di GitHub tanpa Packet Tracer.

Penjelasan rinci tiap file ada di README masing-masing BAB.
