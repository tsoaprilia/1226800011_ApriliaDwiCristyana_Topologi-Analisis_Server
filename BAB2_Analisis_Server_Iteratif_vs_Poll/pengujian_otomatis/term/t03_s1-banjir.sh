cd "$(dirname "$0")/../hasil"; P() { printf "\033[1;32mwindows@WSL\033[0m:\033[1;34m~/uji_server/hasil\033[0m$ %s\n" "$1"; }
P "cat s1-banjir.klien.log"; cat s1-banjir.klien.log
P "cat s1-banjir.ss.txt"; cat s1-banjir.ss.txt
P "grep -c 'terima 512' s1-banjir.server.log"; grep -c 'terima 512' s1-banjir.server.log
P "head -3 s1-banjir.server.log; tail -3 s1-banjir.server.log"; head -3 s1-banjir.server.log; tail -3 s1-banjir.server.log | grep -v Terminated
