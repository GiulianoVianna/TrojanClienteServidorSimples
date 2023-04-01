import os
import socket
import shlex

server_host = '127.0.0.1' #Endereço IP
server_port = 12345       #Porta

def listar_diretorios(sock, diretorio):
    sock.sendall(f"ls {shlex.quote(diretorio)}".encode('utf-8'))
    response = sock.recv(4096).decode('utf-8')
    print(f"Diretório atual: {diretorio}")
    print(response)


def baixar_arquivo(sock, arquivo_remoto, arquivo_local):
    sock.sendall(f"download {arquivo_remoto}".encode('utf-8'))
    with open(arquivo_local, 'wb') as file:
        file_data = sock.recv(1024)
        while file_data:
            file.write(file_data)
            file_data = sock.recv(1024)
    print(f"Arquivo baixado: {arquivo_local}")

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))

    print("Digite 'ls <caminho_do_diretório>' para listar o conteúdo do diretório.")
    print("Digite 'download <arquivo_remoto> <arquivo_local>' para baixar um arquivo.")
    print("Digite 'sair' para encerrar a conexão.")

    while True:
        comando = input("Digite um comando: ")

        if comando.lower() == "sair":
            break

        args = shlex.split(comando)
        cmd = args[0].lower()

        if cmd == "ls":
            diretorio = args[1].strip()
            listar_diretorios(client, diretorio)
        elif cmd == "download":
            arquivo_remoto, arquivo_local = args[1], args[2]
            baixar_arquivo(client, arquivo_remoto, arquivo_local)
            
    client.close()

if __name__ == "__main__":
    main()


