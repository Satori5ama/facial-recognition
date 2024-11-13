import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class Server:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def start(self):



        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connected to {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                self.display_message(data)
            except Exception as e:
                break
        client_socket.close()

    def display_message(self, message):
        app.text_area.insert(tk.END, message + '\n')
        app.text_area.see(tk.END)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Interface")
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    server = Server()
    threading.Thread(target=server.start, daemon=True).start()
    root.mainloop()
