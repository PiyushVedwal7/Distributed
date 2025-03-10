import socket
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading

selected_file = None

def select_file():
    global selected_file
    selected_file = filedialog.askopenfilename(title="Select a File")
    if selected_file:
        file_name = os.path.basename(selected_file)
        file_size = os.path.getsize(selected_file) / 1024  # Convert to KB
        file_label.config(text=f"Selected: {file_name} ({file_size:.2f} KB)", foreground="green")

def split_and_send():
    global selected_file
    if not selected_file:
        messagebox.showerror("Error", "No file selected.")
        return
    
    try:
        status_label.config(text="Reading file...", foreground="blue")
        progress_bar.start()
        root.update_idletasks()

        server1_ip = server1_ip_entry.get()
        server1_port = int(server1_port_entry.get())
        server2_ip = server2_ip_entry.get()
        server2_port = int(server2_port_entry.get())

        with open(selected_file, "rb") as file:
            data = file.read()

        split_ratio = split_slider.get() / 100
        split_index = int(len(data) * split_ratio)
        
        part1 = data[:split_index]
        part2 = data[split_index:]

        part1_path = "client_part1.dat"
        part2_path = "client_part2.dat"

        with open(part1_path, "wb") as f1, open(part2_path, "wb") as f2:
            f1.write(part1)
            f2.write(part2)

        status_label.config(text="Sending files to servers...", foreground="blue")
        
        threading.Thread(target=send_to_server, args=(part1_path, server1_ip, server1_port)).start()
        threading.Thread(target=send_to_server, args=(part2_path, server2_ip, server2_port)).start()

    except Exception as e:
        progress_bar.stop()
        status_label.config(text="File split failed!", foreground="red")
        messagebox.showerror("Error", f"File split failed: {e}")

def send_to_server(file_path, server_ip, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))

        with open(file_path, "rb") as file:
            client_socket.sendall(file.read())
        
        client_socket.close()
        status_label.config(text=f"File sent to {server_ip}:{port}", foreground="green")
        progress_bar.stop()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send file to {server_ip}:{port} - {e}")
        status_label.config(text="Error in file transfer", foreground="red")

# UI Setup
root = tk.Tk()
root.title("Secure File Splitter")
root.geometry("600x500")
root.configure(bg="#2E2E2E")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10, background="#3498db", foreground="white")
style.configure("TLabel", font=("Arial", 11, "bold"), background="#2E2E2E", foreground="white")
style.configure("TFrame", background="#2E2E2E")

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill="both")

title_label = ttk.Label(frame, text="Secure File Splitter", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Server IP & Port Inputs
server_frame = ttk.Frame(frame)
server_frame.pack(pady=5)

ttk.Label(server_frame, text="Server 1 IP:").grid(row=0, column=0, padx=5, pady=2)
server1_ip_entry = ttk.Entry(server_frame, width=15)
server1_ip_entry.grid(row=0, column=1, padx=5)
ttk.Label(server_frame, text="Port:").grid(row=0, column=2, padx=5)
server1_port_entry = ttk.Entry(server_frame, width=5)
server1_port_entry.grid(row=0, column=3, padx=5)

ttk.Label(server_frame, text="Server 2 IP:").grid(row=1, column=0, padx=5, pady=2)
server2_ip_entry = ttk.Entry(server_frame, width=15)
server2_ip_entry.grid(row=1, column=1, padx=5)
ttk.Label(server_frame, text="Port:").grid(row=1, column=2, padx=5)
server2_port_entry = ttk.Entry(server_frame, width=5)
server2_port_entry.grid(row=1, column=3, padx=5)

# File Selection
select_button = ttk.Button(frame, text="Select File", command=select_file)
select_button.pack(pady=5)

file_label = ttk.Label(frame, text="No file selected", foreground="red")
file_label.pack()

# Split Percentage Slider
slider_frame = ttk.Frame(frame)
slider_frame.pack(pady=10)

ttk.Label(slider_frame, text="Split Percentage (Server 1):").pack(side="left", padx=5)
split_slider = ttk.Scale(slider_frame, from_=10, to=90, orient="horizontal", length=200)
split_slider.set(50)
split_slider.pack(side="left")

# Progress Bar
progress_bar = ttk.Progressbar(frame, mode="indeterminate", length=250)
progress_bar.pack(pady=10)

# Send File Button
send_button = ttk.Button(frame, text="Split & Send File", command=split_and_send)
send_button.pack(pady=5)

# Status Label
status_label = ttk.Label(frame, text="Select a file to start.", foreground="white")
status_label.pack(pady=10)

root.mainloop()
