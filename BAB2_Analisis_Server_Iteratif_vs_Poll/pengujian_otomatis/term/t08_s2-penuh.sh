cd "$(dirname "$0")/../hasil"; P() { printf "\033[1;32mwindows@WSL\033[0m:\033[1;34m~/uji_server/hasil\033[0m$ %s\n" "$1"; }
P "tail -4 s2-penuh.klien.log"; tail -4 s2-penuh.klien.log
P "sed -n '30,36p' s2-penuh.server.log"; sed -n '30,36p' s2-penuh.server.log
P "grep -c 'socket error' s2-penuh.server.log"; grep -c 'socket error' s2-penuh.server.log
