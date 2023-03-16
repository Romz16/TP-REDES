import socket
import random
import threading

HOST = "127.0.0.1"

PORT = 55555

# Inicializa o tabuleiro do jogo da velha
board = ['', '', '',
         '', '', '',
         '', '', '']
#conexões 
servidor_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #IPV4 TCP
servidor_socket.bind((HOST,PORT))
clients_sockets = []
servidor_socket.listen(2)
print("aguardando conexão dois  clientes")

# Aceita a conexão do primeiro cliente
cliente1_socket, cliente1_endereco = servidor_socket.accept()
print(f'Conexão estabelecida com {cliente1_endereco}')

# Aceita a conexão do segundo cliente
cliente2_socket, cliente2_endereco = servidor_socket.accept()
print(f'Conexão estabelecida com {cliente2_endereco}')


def send_all(parametro):
    cliente1_socket.send(parametro.encode())
    cliente2_socket.send(parametro.encode())

#Envia para ambos os jogadores com qual simbolo ele irá jogar 
def send_player_symbols():
    global turn,player1_symbol,player2_symbol
    symbols = random.sample(['X', 'O'], k=2)
    player1_symbol = symbols[0]
    player2_symbol = symbols[1]
    print(f"Player 1 will play with symbol {player1_symbol}")
    print(f"Player 2 will play with symbol {player2_symbol}")
    cliente1_socket.send(player1_symbol.encode())
    cliente2_socket.send(player2_symbol.encode())
    turn = player1_symbol

#Verifica se alguem venceu ou perdeu 

def check_game_status():
    # verifica todas as combinações possíveis de vitória e empate
    for i in range(3):
        if (board[i*3] == board[i*3+1] == board[i*3+2] != '') : return board[i*3]
        if (board[i] == board[i+3] == board[i+6] != ''): return board[i]  # retorna o símbolo do jogador vencedor

    if (board[0] == board[4] == board[8] != '') \
    or (board[2] == board[4] == board[6] != ''):
        return board[4]  # retorna o símbolo do jogador vencedor

    if all([cell != '' for cell in board]):
        return "E"  # retorna empate se não houver jogadas disponíveis

    return "C"  # retorna continuar se o jogo ainda não acabou
       
send_player_symbols()

#Envia Quem deverá começar a partida 
first_turn_message = f"{turn}"
send_all(first_turn_message)

def receber_jogada(turn, player_symbol, socket_atual, socket_oponente, board):
    data = socket_atual.recv(3).decode()
    coordinates = data.split('-')
    row = int(coordinates[0])
    col = int(coordinates[1])
    board[row * 3 + col] = player_symbol
    socket_oponente.send(data.encode())
    turn = player2_symbol if turn == player1_symbol else player1_symbol
    return (turn, row, col)


while True:
    # Recebe a jogada do jogador atual
    if turn == player1_symbol:
        turn, row, col = receber_jogada(turn, player1_symbol, cliente1_socket, cliente2_socket, board)
    else:
        turn, row, col = receber_jogada(turn, player2_symbol, cliente2_socket, cliente1_socket, board)
    
    #Verifica se o jogo acabou
    game_status = check_game_status()
    
        # Envie uma mensagem para ambos os jogadores com o resultado do jogo
    send_all(game_status)
    #se n for Continuar, recebe dos dois jogadores sim ou não, caso algum tenha digitado não o jogo fecha 
    print(f"Jogada recebida: {row}{col}")
    
        
    
