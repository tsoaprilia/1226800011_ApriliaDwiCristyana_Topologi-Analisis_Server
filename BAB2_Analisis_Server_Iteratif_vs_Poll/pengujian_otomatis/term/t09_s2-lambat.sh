cd "$(dirname "$0")/../hasil"; P() { printf "\033[1;32mwindows@WSL\033[0m:\033[1;34m~/uji_server/hasil\033[0m$ %s\n" "$1"; }
P "cat s2-lambat.klien.log"; cat s2-lambat.klien.log
P "cat s2-lambat.ss.txt     # saat server membeku"; cat s2-lambat.ss.txt
P "grep PESAN s2-lambat.server.log | cut -c1-20 | uniq -c"; grep PESAN s2-lambat.server.log | cut -c1-20 | uniq -c
P "grep -v PESAN s2-lambat.server.log"; grep -v -e PESAN -e Terminated s2-lambat.server.log
