import socket, threading
from funcoes_socket import *

# Criando o socket TDP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ligando o socket a porta
tcp_socket.connect((HOST_SERVER, SOCKET_PORT))
def enviar_comandos():
    while True:
        mensagem = input('Digite a mensagem (LIST_CLIENTS) para ver os clientes conectados: ').upper()
        print('Aguardando...')

        if mensagem:
            # Convertendo a mensagem digitada de string para bytes
            mensagem = mensagem.encode(CODE_PAGE)
            # Enviando a mensagem ao servidor      
            tcp_socket.send(mensagem)

def receber_repostas():
        while True:
            try:
                # Recebendo echo do servidor
                dado_recebido     = tcp_socket.recv(BUFFER_SIZE)
                if not dado_recebido: break
                mensagem_recebida = dado_recebido.decode(CODE_PAGE)
                print(f'Echo Recebido: {mensagem_recebida}')
            except:
                print('Erro ao receber a resposta do servidor.')
                break

thread_envio = threading.Thread(target=enviar_comandos)
thread_recebimento = threading.Thread(target=receber_repostas)

thread_envio.start()
thread_recebimento.start()

thread_recebimento.join()
thread_envio.join()

# Fechando o socket
tcp_socket.close()
