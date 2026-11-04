cd "$(dirname "$0")/../hasil"; P() { printf "\033[1;32mwindows@WSL\033[0m:\033[1;34m~/uji_server/hasil\033[0m$ %s\n" "$1"; }
P "cat s2-nama.klien.log"; cat s2-nama.klien.log
P "cat s2-nama.server.log"; grep -v Terminated s2-nama.server.log
P "cat s2-panjang.klien.log"; cat s2-panjang.klien.log
P "cat s2-panjang.server.log"; grep -v Terminated s2-panjang.server.log
