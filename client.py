import pygame
from tkinter import messagebox
import socket
import pyautogui
from pygame.locals import *
from playsound import playsound
HOST = "192.168.2.8"
#HOST = "127.0.0.1"
PORT = 55555

WAIT_MSG = "[SERVER] is waiting for another player..."

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #IPV4 TCP
s.connect((HOST,PORT))
print(f"You connected to {HOST}")

# Recebe o símbolo do jogador
symbol = s.recv(1).decode()
print(f"You will play with symbol {symbol}")

# Recebe o turno do servidor
first_turn = s.recv(1).decode()
print(f"First turn is for {first_turn}")

# Define o título da janela do jogo
pygame.display.set_caption(f"Jogo da Velha - Jogador {symbol}")

# Largura e altura de cada célula
cell_width = 200
cell_height = 200

# Tamanho da janela do jogo
window_width = cell_width * 3
window_height = cell_height * 3

#Cores
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
# rgb: red green blue
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Inicializa o pygame
pygame.init()
# Lista que representa o tabuleiro do jogo
board = [['', '', ''], ['', '', ''], ['', '', '']]

# Cria a janela do jogo
screen = pygame.display.set_mode((window_width, window_height))

#Desenha tela
def draw_board():
    # Limpa a tela
    screen.fill(BG_COLOR)
    
    for row in range(3):
        for col in range(3):
            # Desenha o quadrado branco da célula
            pygame.draw.rect(screen, LINE_COLOR, (col * cell_width, row * cell_height, cell_width, cell_height), 2)
            # Desenha a marca (X ou O) na célula, se houver
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )


# Definição da fonte
font = pygame.font.Font(None, 36)
#setup a rectangle for "Play Again" Option
again_rect = Rect(window_width // 2 - 80, window_height // 2, 160, 50)

             
#RESTART
#ssssssssssssssssssss
def reset_board():
    # Define todas as posições do tabuleiro como vazio
    for i in range(3):
        for j in range(3):
            board[i][j] = ''

    # Limpa a tela do jogo
    screen.fill((255, 255, 255)) # Define a cor de fundo para branco

    # Desenha as linhas do tabuleiro novamente
    pygame.draw.line(screen, (0, 0, 0), (100, 0), (100, 300), 2)
    pygame.draw.line(screen, (0, 0, 0), (200, 0), (200, 300), 2)
    pygame.draw.line(screen, (0, 0, 0), (0, 100), (300, 100), 2)
    pygame.draw.line(screen, (0, 0, 0), (0, 200), (300, 200), 2)

    # Atualiza a tela do jogo
    pygame.display.flip()
   
# Roda o jogo da velha


        
def run_game():
    turn = first_turn
    pyautogui.alert(text=f'JOGADOR {first_turn} É O PRIMEIRO A JOGAR', title='PRIMEIRO_TURNO', button='OK')
    game_status = "C"
    pygame.mixer.music.load('sons/Inicio.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.load('sons/Intro.mp3')
    pygame.mixer.music.play()
    
    
    # Loop principal do jogo
    while True:
        draw_board()
      #Verifica estado do jogo 
        if game_status =="C":
      #verifica se o turno atual é do cliente 
            if turn == symbol:
                jogada_valida = False
                while not jogada_valida:
                    draw_board()
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                # Obtém a posição do clique do mouse
                            pos = pygame.mouse.get_pos()
                                # Calcula a linha e coluna da célula clicada
                            col = pos[0] // cell_width
                            row = pos[1] // cell_height
                                # Marca a célula com o símbolo do jogador atual
                            if board[row][col] == '' and game_status =="C":
                                board[row][col] = symbol
                            else:
                                print("JOGADA INVALIDA")
                                continue
                            # Atualiza a tela com o novo estado do jogo
                            jogada_valida = True
                            send_data = f'{row}-{col}'.encode()
                            s.send(send_data)             
                        
                            draw_board()
                            pygame.display.update()
                            #troca turnos 
                            if turn == 'X':
                                turn= 'O' 
                            else :
                                turn = 'X'
            #Espera jogada do opnonete
            else:
                draw_board()
                pygame.display.update()
                jogada_oponente = s.recv(3).decode()
                coordinates = jogada_oponente.split('-')
                row, col = int(coordinates[0]), int(coordinates[1])
                
                if board[row][col] == '':
                        board[row][col] = turn
                else:
                    print("JOGADA INVALIDA")
                    continue
                draw_board()
                pygame.display.update()
                    #troca turnos 
                if turn == 'X':
                    turn = 'O' 
                else :
                    turn = 'X'
                    
            game_status = s.recv(1).decode()
            if game_status =="C":
                 if game_status == "X" or game_status == "O":
                    pygame.mixer.music.load('sons/Final.mp3')
                    pygame.mixer.music.play()
                    print(f'{game_status} VENCEU')
                    if symbol == game_status:
                        pyautogui.alert(text=f'JOGADOR {game_status} É O VENCEDOR!!\n VOCÊ VENCEU', title='VENCEDOR', button='OK')
                    else:
                        pyautogui.alert(text=f'JOGADOR {game_status} É O VENCEDOR!!\n VOCÊ PERDEU', title='VENCEDOR', button='OK')
                    
                 if game_status =="E":
                    pygame.mixer.music.load('sons/Empate.mp3')
                    pygame.mixer.music.play()
                    pyautogui.alert(text=f'Não houve vencedor, EMPATE!', title='EMPATE', button='OK')
                 continue
        
        print(f"Game status: {game_status}")
       
        
        resp = messagebox.askyesno("RESET","REINICIAR JOGO?")
        
        if bool(resp)== False:
            s.send("N".encode())
            quit()
        else:
            s.send("S".encode())
            server_resp = s.recv(1).decode()
            if server_resp =="S":
                reset_board()
                game_status ="C"
                jogada_valida = False
                pyautogui.alert(text=f'JOGADOR {turn} É O PRIMEIRO A JOGAR', title='PRIMEIRO_TURNO', button='OK')
            else:
                pyautogui.alert(text=f'O outro jogador não quer reiniciar partida', title='RESULTADO', button='OK')
                quit()
        print("ULTIMO GAME STATUS",game_status)
        for i in range(3):
            for j in range(3):
                print(f'"{board[i][j]}"')
        pygame.display.flip()
       

# Inicia o jogo
draw_board()
pygame.display.update()
run_game()