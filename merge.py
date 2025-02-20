import socket
import threading
import os
import tkinter as tk
from tkinter import messagebox, ttk

# Server Configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 6054

PART1_PATH = "client_part1.dat"
PART2_PATH = "client_part2.dat"
MERGED_FILE_PATH = "merged_file.dat"


# 🟢 SERVER FUNCTIONALITY
def merge_files():
    """Merge part1 and part2 files into a single file."""
    if not os.path.exists(PART1_PATH) or not os.path.exists(PART2_PATH):
        print("Error: One or both file parts are missing.")
        return False  # Merge failed

    try:
        with open(MERGED_FILE_PATH, "wb") as final_file:
            with open(PART1_PATH, "rb") as f1:
                final_file.write(f1.read())
            with open(PART2_PATH, "rb") as f2:
                final_file.write(f2.read())

        print(f"✅ Merged file saved as {MERGED_FILE_PATH}")
        return True  # Merge success
    except Exception as e:
        print(f"❌ Error merging files: {e}")
        return False


def handle_client(conn):
    """Handle incoming merge requests from the client."""
    try:
        data = conn.recv(1024)
        if data and data.decode() == "MERGE_REQUEST":
            if merge_files():
                with open(MERGED_FILE_PATH, "rb") as merged_file:
                    conn.sendall(merged_file.read())
                print("✅ Merged file sent to client.")
            else:
                conn.sendall(b"ERROR: Merge failed.")
    except Exception as e:
        print(f"❌ Client handling error: {e}")
    finally:
        conn.close()


def start_server():
    """Start the file merge server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((SERVER_IP, SERVER_PORT))
    except Exception as e:
        print(f"❌ Server binding error: {e}")
        return

    server_socket.listen(5)
    print(f"🚀 Merge Server running on {SERVER_IP}:{SERVER_PORT}")

    while True:
        try:
            conn, addr = server_socket.accept()
            print(f"🔗 Connection received from {addr}")
            threading.Thread(target=handle_client, args=(conn,)).start()
        except Exception as e:
            print(f"❌ Error accepting connection: {e}")


# 🔹 Start server in a separate thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()


# 🟢 CLIENT/UI FUNCTIONALITY
def request_merge():
    """Request the server to merge files and retrieve the merged file."""
    try:
        status_label.config(text="Requesting merge...", foreground="blue")
        root.update_idletasks()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        client_socket.sendall(b"MERGE_REQUEST")

        response = client_socket.recv(1024)  # Get response first
        if response.startswith(b"ERROR"):
            raise Exception(response.decode())

        with open(MERGED_FILE_PATH, "wb") as merged_file:
            merged_file.write(response)  # Write merged file

        client_socket.close()

        status_label.config(text="✅ Files merged successfully!", foreground="green")
        messagebox.showinfo("Success", f"Merged file saved as {MERGED_FILE_PATH}")
    except Exception as e:
        status_label.config(text="❌ Merge failed!", foreground="red")
        messagebox.showerror("Error", f"Merge failed: {e}")


# 🔹 UI Setup
root = tk.Tk()
root.title("File Merger")
root.geometry("500x400")
root.configure(bg="#2E2E2E")  # Dark mode background

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 11, "bold"), background="#2E2E2E", foreground="white")
style.configure("TFrame", background="#2E2E2E")

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill="both")

title_label = ttk.Label(frame, text="File Merger", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Merge Button
merge_button = ttk.Button(frame, text="Merge Files", command=request_merge)
merge_button.pack(pady=10)

# Status Label
status_label = ttk.Label(frame, text="Click 'Merge Files' to start.", foreground="white")
status_label.pack(pady=10)

root.mainloop()
