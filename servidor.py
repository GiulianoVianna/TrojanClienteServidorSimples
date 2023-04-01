import os
import socket
import shlex

server_host = '127.0.0.1' #Endereço IP
server_port = 12345       #Porta

def send_file(client_socket, file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read(1024)
            while file_data:
                client_socket.send(file_data)
                file_data = file.read(1024)
            client_socket.send(b'')
    except Exception as e:
        client_socket.send(f"Erro: {str(e)}".encode('utf-8'))

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Comando recebido: {data}")

        args = shlex.split(data)
        cmd = args[0].lower()

        if cmd == "ls":
            path = args[1].strip()
            try:
                files = os.listdir(path)
                response = '\n'.join(files)
            except Exception as e:
                response = f"Erro: {str(e)}"
            client_socket.send(response.encode('utf-8'))
        elif cmd == "download":
            file_path = args[1].strip()
            send_file(client_socket, file_path)
              
            

    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_host, server_port))
    server.listen(5)
    print(f"[*] Servidor ouvindo em {server_host}:{server_port}")

    while True:
        client, addr = server.accept()
        print(f"[*] Conexão estabelecida com {addr[0]}:{addr[1]}")
        handle_client(client)

    server.close()

if __name__ == "__main__":
    main()
