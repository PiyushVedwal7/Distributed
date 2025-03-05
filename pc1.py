import socket
import os
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog

server_socket = None  
ADMIN_PASSWORD = "secure123"  

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def start_server():
    global server_socket
    try:
        server_ip = get_local_ip()
        ip_label.config(text=f"Server IP: {server_ip}")
        SERVER1_PORT = 8082
        SAVE_DIR = "server1_storage"
        os.makedirs(SAVE_DIR, exist_ok=True)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, SERVER1_PORT))
        server_socket.listen(5)
        status_label.config(text=f"Server listening on {server_ip}:{SERVER1_PORT}", fg="green")

        while server_socket:
            try:
                conn, addr = server_socket.accept()
                data = conn.recv(4096)
                if data:
                    file_path = os.path.join(SAVE_DIR, "file_part1.dat")
                    with open(file_path, "ab") as f:
                        f.write(data)
                    status_label.config(text=f"Part 1 received and saved at {file_path}")
                conn.close()
            except OSError:
                break  # Exit the loop when the socket is closed
    except Exception as e:
        status_label.config(text=f"Error: {e}", fg="red")

def authenticate_and_run():
    password = simpledialog.askstring("Authentication", "Enter Admin Password:", show="*")
    if password == ADMIN_PASSWORD:
        threading.Thread(target=start_server, daemon=True).start()
        messagebox.showinfo("Server Status", "Server started successfully!")
    else:
        messagebox.showerror("Access Denied", "Incorrect password!")

def stop_server():
    global server_socket
    if server_socket:
        try:
            server_socket.close()
            server_socket = None
            status_label.config(text="Server stopped", fg="red")
            messagebox.showinfo("Server Status", "Server stopped successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error stopping server: {e}")

# UI Setup
root = tk.Tk()
root.title("File Receiver Server")
root.geometry("450x300")
root.configure(bg="#f4f4f4")

frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief=tk.RIDGE, bd=2)
frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Title Label
title_label = tk.Label(frame, text="File Receiver Server", font=("Arial", 16, "bold"), bg="#ffffff")
title_label.pack(pady=10)

# IP Address Label
ip_label = tk.Label(frame, text=f"Server IP: {get_local_ip()}", font=("Arial", 12), bg="#ffffff", fg="#333")
ip_label.pack()

# Server Status Label
status_label = tk.Label(frame, text="Server not running", font=("Arial", 12, "bold"), bg="#ffffff", fg="red")
status_label.pack(pady=10)

# Button Frame
button_frame = tk.Frame(frame, bg="#ffffff")
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start Server", command=authenticate_and_run, font=("Arial", 12), bg="#28a745", fg="white", padx=10, pady=5, width=15)
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(button_frame, text="Stop Server", command=stop_server, font=("Arial", 12), bg="#dc3545", fg="white", padx=10, pady=5, width=15)
stop_button.grid(row=0, column=1, padx=5)

root.mainloop()
