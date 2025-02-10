import socket
import os

SERVER1_IP = "127.0.0.1"
SERVER1_PORT = 8082
SAVE_DIR = "server1_storage"

os.makedirs(SAVE_DIR, exist_ok=True)

def start_server1():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER1_IP, SERVER1_PORT))
    server_socket.listen(5)
    print(f"Server 1 listening on {SERVER1_IP}:{SERVER1_PORT}")

    while True:
        conn, addr = server_socket.accept()
        data = conn.recv(4096)
        if data:
            file_path = os.path.join(SAVE_DIR, "file_part1.dat")
            with open(file_path, "ab") as f:
                f.write(data)
            print(f"Part 1 received and saved at {file_path}")

        conn.close()

if __name__ == "__main__":
    start_server1()
