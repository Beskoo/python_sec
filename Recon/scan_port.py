import socket


target_ip = "127.0.0.1" 
start_port = 1
end_port = 1024


def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((host, port))
            print(f"Port {port} est ouvert")
    except (socket.timeout, ConnectionRefusedError):
        print(f"Port {port} est fermé")

# Fonction principale
def main():
    print(f"Scanning des ports de {start_port} à {end_port} sur {target_ip}...")
    for port in range(start_port, end_port + 1):
        scan_port(target_ip, port)

if __name__ == "__main__":
    main()