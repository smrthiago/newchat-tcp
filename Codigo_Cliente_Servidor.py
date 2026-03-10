# Código Servidor 
import socket
import base64
import threading # Necessário para múltiplos clientes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def gerar_chave(senha: str):
    salt = b'aula_infra' 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(senha.encode()))

# Função que gerencia cada cliente individualmente
def handle_client(conn, addr, cipher):
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    while True:
        try:
            dados_recebidos = conn.recv(1024)
            if not dados_recebidos:
                break
            
            mensagem_clara = cipher.decrypt(dados_recebidos).decode()
            print(f"[{addr}]: {mensagem_clara}")
            
        except Exception:
            break
    
    print(f"[DESCONECTADO] {addr} saiu.")
    conn.close()

# Configuração Inicial
senha_input = input("Defina a senha para descriptografar: ")
cipher = Fernet(gerar_chave(senha_input))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 5000))
server.listen() # Removido o limite de 1 para aceitar múltiplos

print("\n[SERVIDOR ATIVO] Aguardando conexões múltiplas...")

while True:
    conn, addr = server.accept()
    # Cria uma Thread para o novo cliente e volta a ouvir a porta 5000
    thread = threading.Thread(target=handle_client, args=(conn, addr, cipher))
    thread.start()

#Codigo Cliente 
import socket
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def gerar_chave(senha: str):
    salt = b'aula_infra'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(senha.encode()))

# Configuração Inicial
ip_alvo = input("Digite o IP do servidor (ex: 192.168.1.15): ")
senha_input = input("Digite a senha de criptografia: ")
cipher = Fernet(gerar_chave(senha_input))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((ip_alvo, 5000))
    print("\n[CONECTADO COM SUCESSO]")
    
    while True:
        mensagem = input("Digite a mensagem (ou 'sair'): ")
        if mensagem.lower() == 'sair':
            break
        
        # Criptografia antes do envio
        token_criptografado = cipher.encrypt(mensagem.encode())
        client.sendall(token_criptografado)
        
except Exception as e:
    print(f"[ERRO]: Não foi possível conectar. Verifique o IP e o Firewall. {e}")

finally:
    client.close()
