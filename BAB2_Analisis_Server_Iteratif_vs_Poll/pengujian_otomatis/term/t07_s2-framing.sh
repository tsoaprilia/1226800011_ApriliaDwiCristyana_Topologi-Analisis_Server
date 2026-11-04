cd "$(dirname "$0")/../hasil"; P() { printf "\033[1;32mwindows@WSL\033[0m:\033[1;34m~/uji_server/hasil\033[0m$ %s\n" "$1"; }
P "cat s2-pecah.klien.log"; cat s2-pecah.klien.log
P "cat s2-gabung.klien.log"; cat s2-gabung.klien.log
P "grep PESAN s2-pecah.server.log s2-gabung.server.log"; grep PESAN s2-pecah.server.log s2-gabung.server.log
P "cat s1-pecah.klien.log    # pembanding: S1"; cat s1-pecah.klien.log
