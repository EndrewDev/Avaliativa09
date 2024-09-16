import socket, platform, threading
from funcoes_socket import *
from funcao_tracrt import *

sisOp = platform.system()

print('Servidor aguardando conexões...\n')

print('Recebendo Mensagens...\n\n')

# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ligando o socket a porta
tcp_socket.bind((HOST_SERVER, SOCKET_PORT)) 

# Máximo de conexões enfileiradas
tcp_socket.listen(MAX_LISTEN)

clientes_conectados = []

def clientes(conexao, cliente):
    clientes_conectados.append(cliente)
    print('Conectado por: ', cliente)
    while True:
        # Aceita a conexão com o cliente        
        try:
            mensagem = conexao.recv(BUFFER_SIZE)
            if not mensagem: break
            mensagem_decode = mensagem.decode(CODE_PAGE)
            print(cliente, mensagem_decode)
        
            # Verificar sse o comando é para listar clientes
            if mensagem_decode == 'LIST_CLIENTS':
                clientes_info = '\n'.join([f'{ip}:{porta}' for ip, porta in clientes_conectados])
                conexao.send(f'Cliente conectados:\n{clientes_info}'.encode(CODE_PAGE))
            else:            
                # Devolvendo uma mensagem (echo) ao cliente
                mensagem_executar = tracert_to_url(mensagem, sisOp)
                cria_arquivo(mensagem_decode, mensagem_executar)
                print(mensagem_executar)
                mensagem_retorno = 'Devolvendo...' + mensagem.decode(CODE_PAGE) + '\nJá está salvo do arquivo forma de JSON.'
                conexao.send(mensagem_retorno.encode(CODE_PAGE))
        except ConnectionResetError:
            print(f'Cliente {cliente} desconectou abruptamente.')
            break
    
    clientes_conectados.remove(cliente)
    print('Finalizando Conexão do Cliente ', cliente)
    conexao.close()

while True:
    conexao, cliente = tcp_socket.accept()
    cliente_thread = threading.Thread(target=clientes, args=(conexao, cliente))
    cliente_thread.start()