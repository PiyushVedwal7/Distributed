import socket
import os

SERVER2_IP = "127.0.0.1"
SERVER2_PORT = 9090
SAVE_DIR = "server2_storage"

os.makedirs(SAVE_DIR, exist_ok=True)

def start_server2():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER2_IP, SERVER2_PORT))
    server_socket.listen(5)
    print(f"Server 2 listening on {SERVER2_IP}:{SERVER2_PORT}")

    while True:
        conn, addr = server_socket.accept()
        data = conn.recv(4096)
        if data:
            file_path = os.path.join(SAVE_DIR, "file_part2.dat")
            with open(file_path, "ab") as f:
                f.write(data)
            print(f"Part 2 received and saved at {file_path}")

        conn.close()

if __name__ == "__main__":
    start_server2()
