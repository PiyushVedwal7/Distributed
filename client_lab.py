import socket

PC1_IP = "192.168.96.195"  # Replace with PC1's actual IP
PC1_PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((PC1_IP, PC1_PORT))

message = "Hello from Client!"
client_socket.sendall(message.encode())

print("Message sent to Server 1")
client_socket.close()
