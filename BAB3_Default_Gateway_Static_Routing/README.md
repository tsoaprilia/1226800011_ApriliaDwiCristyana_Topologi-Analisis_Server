# BAB 3 – Menguji dan Menganalisa Fungsi Default Gateway

Topologi dari papan tulis dibuat ulang di Packet Tracer dengan **routing statis biasa**, lalu fungsi default gateway dianalisa dari hasil komunikasi antar-PC. Laporan lengkap ada di [`../laporan/Laporan Praktikum Jaringan - BAB 1-3.docx`](../laporan/) (BAB 3).

## Isi folder

| File / folder | Keterangan |
|---|---|
| `Static_Routing_Default_Gateway_v3.pkt` | Topologi Packet Tracer final, berisi 6 PDU uji untuk semua pasangan PC |
| `konfigurasi/R0_running-config.txt` | Running-config R0, diekstrak dari file `.pkt` |
| `konfigurasi/R1_running-config.txt` | Running-config R1, diekstrak dari file `.pkt` |
| `screenshot/` | Bukti pengujian (semua diambil dari file v3) |

## Topologi dan pengalamatan

2 router Cisco 2911, 3 switch 2960, 4 PC, tiga LAN yang dihubungkan link WAN /30.

| Perangkat | Interface | Alamat IP | Default gateway |
|---|---|---|---|
| R0 | Gi0/0 (LAN 5) | 192.168.5.1/24 | – |
| R0 | Gi0/1 (ke R1) | 192.168.3.241/30 | – |
| R1 | Gi0/1 (ke R0) | 192.168.3.242/30 | – |
| R1 | Gi0/0 (LAN 1) | 192.168.1.1/24 | – |
| R1 | Gi0/2 (LAN 2) | 192.168.2.1/24 | – |
| PC0 / PC1 | Fa0 | 192.168.5.2 / .3 | 192.168.5.1 |
| PC2 | Fa0 | 192.168.1.2 | 192.168.1.1 |
| PC3 | Fa0 | 192.168.2.2 | 192.168.2.1 |

Route statis:

```
R0(config)# ip route 192.168.1.0 255.255.255.0 192.168.3.242
R0(config)# ip route 192.168.2.0 255.255.255.0 192.168.3.242
R1(config)# ip route 192.168.5.0 255.255.255.0 192.168.3.241
```

## Hasil pengujian

| Skenario | Gateway PC0 | Ping PC1 (satu LAN) | Ping PC2 / PC3 (LAN lain) | ARP PC0 |
|---|---|---|---|---|
| A. Benar | 192.168.5.1 | Berhasil, TTL=128 | Berhasil, TTL=126 | 192.168.5.1 = 0003.e4e0.d301 |
| B. Kosong | 0.0.0.0 | Berhasil, TTL=128 | Gagal 100% | – |
| C. Salah | 192.168.5.9 | – | Gagal 100% | No ARP Entries Found |

Mode Simulation membuktikan bahwa frame PC0 → PC3 memakai **MAC R0 (0003.E4E0.D301)** sebagai tujuan Layer 2, sedangkan IP tujuan Layer 3 tetap 192.168.2.2.

### Simulasi PDU (6 pasangan PC)

| PDU | Tembakan pertama | Tembakan ulang |
|---|---|---|
| PC0 → PC1 | Successful | – |
| PC0 → PC2 | Failed | Successful |
| PC0 → PC3 | Failed | Successful |
| PC1 → PC2 | Failed | Successful |
| PC1 → PC3 | Successful | – |
| PC2 → PC3 | Successful | – |

Failed pada tembakan pertama **bukan** kesalahan konfigurasi. Packet Tracer tidak menyimpan tabel ARP ke file, sehingga router membuang paket pertama selagi mencari MAC tujuan. Setelah ARP terisi, semua PDU Successful.

**Cara mengulang:** buka file, tunggu sekitar 30 detik sampai lampu switch hijau, double-click **Fire** pada tiap PDU, lalu ulangi Fire untuk PDU yang Failed.

## Daftar screenshot

| File | Isi |
|---|---|
| `01_topologi_v3.png` | Topologi berlabel |
| `02`, `03_*_show_ip_interface_brief.png` | Status interface R0 dan R1 |
| `04`, `05_*_running_config.png` | Interface dan route statis R0 dan R1 |
| `06_PC0_ipconfig_gateway_benar.png` | IP Configuration PC0 normal |
| `07_skenarioA_ping_tracert_arp.png` | Skenario A: ping, tracert, arp dengan gateway benar |
| `08`, `09_*gateway_kosong*.png` | Skenario B: gateway dikosongkan |
| `10`, `11_*gateway_salah*.png` | Skenario C: gateway 192.168.5.9 |
| `12_gateway_dikembalikan_ping_tracert.png` | Ping dan tracert setelah gateway dikembalikan |
| `13_arp_PC0_MAC_gateway.png` | Tabel ARP PC0 berisi MAC gateway |
| `14`, `15_*_show_ip_route.png` | Tabel routing R0 dan R1 |
| `16_sim_PC0_ke_PC1_ARP_broadcast.png` | Simulation: ARP broadcast untuk tujuan satu LAN |
| `17_sim_PC0_ke_PC3_MAC_gateway.png` | Simulation: frame ke LAN lain ditujukan ke MAC R0 |
| `18_sim_PC0_ke_PC3_detail_IP.png` | Simulation: detail Ethernet dan IP |
| `19`–`22_PDU_*.png` | Daftar PDU: sukses satu LAN, failed pertama, semua successful |
