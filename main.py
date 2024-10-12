import socket
import os
import argparse

def get_local_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def send_file(file_path, port=9000):
    """Sets up a socket server and sends the file when a client connects"""
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("", port))
        server_socket.listen(1)

        print(f"Serving file on http://{get_local_ip()}:{port}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connection from {addr}")

            headers = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: application/octet-stream\r\n"
                f"Content-Disposition: attachment; filename={file_name}\r\n"
                f"Content-Length: {file_size}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            )
            conn.sendall(headers.encode())
            print(f"Sent headers:\n{headers}")

            with open(file_path, "rb") as file:
                while chunk := file.read(1024):
                    conn.sendall(chunk)

            print("File transfer complete.")

            conn.shutdown(socket.SHUT_RDWR)
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a file over LAN via socket")
    parser.add_argument("file", help="The file to transfer")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print("Error: File does not exist.")
        exit(1)

    send_file(args.file)