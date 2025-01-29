import socket
import threading

# Update with PC1 and PC2 IPs (found using ipconfig/ifconfig)
PC1_IP = "192.168.96.100"  # Replace with PC1's actual IP
PC1_PORT = 8082

PC2_IP = "192.168.43.101"  # Replace with PC2's actual IP
PC2_PORT = 9090

def forward_data_to_server_2(data):
    """Forwards received data to PC2 (Server 2)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket_2:
            server_socket_2.connect((PC2_IP, PC2_PORT))
            server_socket_2.sendall(data)
            print(f"Data forwarded to Server 2: {data.decode()}")
    except Exception as e:
        print(f"Error forwarding data to Server 2: {e}")

def handle_client(client_socket, client_address):
    """Handles client connection."""
    print(f"Connection received from {client_address}")
    
    try:
        data = client_socket.recv(1024)
        if data:
            print(f"Data received from Client: {data.decode()}")
            forward_data_to_server_2(data)
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    
    client_socket.close()

def start_server_1():
    """Starts Server 1 to listen for client connections."""
    server_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server_socket_1.bind((PC1_IP, PC1_PORT))
        server_socket_1.listen(5)
        print(f"Server 1 is listening on {PC1_IP}:{PC1_PORT}")

        while True:
            client_socket, client_address = server_socket_1.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    
    except Exception as e:
        print(f"Error starting Server 1: {e}")
    finally:
        server_socket_1.close()

if __name__ == "__main__":
    start_server_1()
