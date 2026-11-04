cd "$(dirname "$0")/../hasil"; P() { printf "\033[1;32mwindows@WSL\033[0m:\033[1;34m~/uji_server/hasil\033[0m$ %s\n" "$1"; }
P "cat s1-dua.server.log"; grep -v Terminated s1-dua.server.log
P "cat s1-dua.ss.txt     # diambil saat B menunggu"; cat s1-dua.ss.txt
P "cat s1-dua.klien.log"; cat s1-dua.klien.log
