# BAB 1 – Menerapkan dan Menganalisa RIP (Dynamic Routing)

Routing statis pada topologi dua router diganti dengan **RIP versi 2**, lalu perbedaan cara router mendapatkan rute dianalisa. Laporan lengkap ada di [`../laporan/Laporan Praktikum Jaringan - BAB 1-3.docx`](../laporan/) (BAB 1).

## Isi folder

| File / folder | Keterangan |
|---|---|
| `RIP_Dynamic_Routing_v2.pkt` | Topologi Packet Tracer dengan konfigurasi RIP v2 yang sudah final |
| `konfigurasi/Router0_running-config.txt` | Running-config Router0, diekstrak dari file `.pkt` |
| `konfigurasi/Router1_running-config.txt` | Running-config Router1, diekstrak dari file `.pkt` |
| `screenshot/` | Bukti proses dan hasil pengujian (Gambar 1.1–1.15 di laporan) |

## Topologi dan pengalamatan

Dua router Cisco 1941 dihubungkan lewat jaringan 192.168.3.0/24; masing-masing melayani satu LAN lewat switch 2950-24.

| Perangkat | Interface | Alamat IP | Default gateway |
|---|---|---|---|
| Router0 | Gi0/0 (LAN 1) | 192.168.1.1/24 | – |
| Router0 | Gi0/1 (penghubung) | 192.168.3.1/24 | – |
| Router1 | Gi0/0 (LAN 2) | 192.168.2.1/24 | – |
| Router1 | Gi0/1 (penghubung) | 192.168.3.2/24 | – |
| PC0 / PC1 / PC4 | Fa0 | 192.168.1.10 / .20 / .30 | 192.168.1.1 |
| PC2 / PC3 | Fa0 | 192.168.2.10 / .20 | 192.168.2.1 |

## Konfigurasi RIP

```
Router0(config)# router rip
Router0(config-router)# version 2
Router0(config-router)# no auto-summary
Router0(config-router)# network 192.168.1.0
Router0(config-router)# network 192.168.3.0
Router0(config-router)# passive-interface GigabitEthernet0/0
```

Router1 sama, tetapi mengumumkan `network 192.168.2.0` dan `network 192.168.3.0`. Route statis lama harus dihapus (`no ip route ...`) karena administrative distance-nya (1) lebih diutamakan daripada RIP (120).

## Hasil utama

| Uji | Hasil |
|---|---|
| `show ip route` Router0 | `R 192.168.2.0/24 [120/1] via 192.168.3.2` |
| `show ip route` Router1 | `R 192.168.1.0/24 [120/1] via 192.168.3.1` |
| `show ip protocols` | RIP v2, update 30 s, invalid 180 s, flush 240 s, passive Gi0/0 |
| Ping PC0 → PC2/PC3 | Berhasil, TTL=126 (1 timeout awal karena ARP) |
| Gi0/0 Router1 di-shutdown | Router0 menandai 192.168.2.0/24 *possibly down* |
| Gi0/0 Router1 di-no shutdown | Rute R kembali otomatis |

## Daftar screenshot

| File | Isi |
|---|---|
| `01_topologi_RIP.png` | Topologi lengkap berlabel interface dan IP |
| `02`–`05_palet_*.png` | Palet perangkat: router, switch, end device, kabel |
| `06_PC0_ip_configuration.png` | IP Configuration PC0 |
| `07_Router0_ip_interface_brief.png` | `show ip interface brief` Router0 |
| `08`, `09_Router*_running_config.png` | Running-config Router0 dan Router1 (blok `router rip`) |
| `10`, `11_Router*_show_ip_route.png` | Tabel routing dengan rute R |
| `12_Router0_show_ip_protocols.png` | Parameter RIP |
| `13_link_down_possibly_down.png` | Rute ditandai possibly down saat link LAN 2 mati |
| `14_link_up_rute_kembali.png` | Rute kembali otomatis saat link hidup |
| `15_PC0_ping_tracert.png` | Ping dan tracert dari PC0 ke LAN 2 |
