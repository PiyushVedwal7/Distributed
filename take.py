import socket

# Listen on all available network interfaces
PC2_IP = "0.0.0.0"  # 0.0.0.0 makes it accessible from any IP
PC2_PORT = 8082

def start_server_2():
    """Starts Server 2 to receive data from another PC on the same network."""
    server_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Allow reusing the address (helps avoid 'Address already in use' error)
        server_socket_2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to all available interfaces on the specified port
        server_socket_2.bind((PC2_IP, PC2_PORT))
        server_socket_2.listen(5)
        print(f"Server 2 is listening on {PC2_PORT} (accepting connections from any IP in the network)")

        while True:
            client_socket, client_address = server_socket_2.accept()
            print(f"Connection established with {client_address}")

            data = client_socket.recv(1024)
            if data:
                print(f"Data received: {data.decode()}")
            
            client_socket.close()
    
    except Exception as e:
        print(f"Error in Server 2: {e}")
    
    finally:
        server_socket_2.close()

if __name__ == "__main__":
    start_server_2()
