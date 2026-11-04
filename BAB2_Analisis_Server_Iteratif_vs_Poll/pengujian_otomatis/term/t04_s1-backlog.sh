cd "$(dirname "$0")/../hasil"; P() { printf "\033[1;32mwindows@WSL\033[0m:\033[1;34m~/uji_server/hasil\033[0m$ %s\n" "$1"; }
P "cat s1-backlog.ss.txt     # detik ke-3, A masih dilayani"; cat s1-backlog.ss.txt
P "grep -c MASUK s1-backlog.server.log"; grep -c MASUK s1-backlog.server.log
