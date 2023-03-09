import socket
import threading
import sys
import random 

# Server IP and port
HOST = "127.0.0.1"
PORT = 55555
list = ["O","X"]
turn = random.choice(list)

# Socket type and options
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



# dictionary of client sockets and their nicknames
clients = {}

def handle_client(conn, addr, clients):
    with conn:
        print(f'Novo cliente conectado: {addr}')
        clients.append(conn)

        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode().strip()
            print(f'Recebido de {addr}: {message}')

            if message == 'reset':
                # Envia mensagem para o outro cliente
                other_clients = [c for c in clients if c != conn]
                for client in other_clients:
                    client.sendall(b'reset\n')

                # Espera a resposta do outro cliente
                for client in other_clients:
                    response = client.recv(1024).decode().strip()
                    print(f'Recebido de {client.getpeername()}: {response}')
                    if response == 'nao':
                        conn.sendall(b'NAO\n')
                        return
                conn.sendall(b'SIM\n')

        print(f'Cliente desconectado: {addr}')
        clients.remove(conn)

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f'Servidor iniciado em {HOST}:{PORT}')

        clients = []
        while True:
            global turn
            # Accept Connection
            conn,addr= s.accept()
            print("Connected with {}".format(str(addr)))
            s.send(turn.encode('utf-8'))
            nickname = f'player {turn}'
            if turn == "X":
                turn = "O"
            elif turn == "O":
                turn = "X"
            # # Request And Store Nickname
            # client_socket.send("/id".encode("utf-8"))
            # nickname = client_socket.recv(1024).decode("utf-8")
            # Add client info to the dictionary
            clients.update({s: nickname})
            # Start Handling Thread For Client
            thread = threading.Thread(target=handle_client, args=(s,))
            thread.start()
            

if __name__ == '__main__':
    run_server()