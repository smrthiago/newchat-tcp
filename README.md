# Chat-TCP
Este projeto consiste em uma aplicação de chat cliente-servidor desenvolvida em Python para a disciplina de Infraestrutura em Redes (2401-SOFTWARE-N05). O sistema permite a comunicação entre múltiplas instâncias através de sockets nativos, garantindo a confidencialidade dos dados via criptografia simétrica.

## Objetivos Atendidos:
  1. *Arquitetura Cliente-Servidor*: Separação clara entre provedor de serviço (Server) e
    consumidores (Clients).
  2. *Comunicação via Sockets*: Implementação manual utilizando a biblioteca nativa socket.
  3. *Protocolo de Transporte*: Utilização de TCP (SOCK_STREAM) para garantir a integridade
    e entrega dos pacotes.
  4. *Concorrência*: Servidor multi-thread capaz de gerenciar múltiplas conexões simultâneas.
  5. *Criptografia Aplicada*: Implementação de padrão AES-128 para proteção de dados em
    trânsito.

## Detalhamento da Criptografia e Chave:
Conforme os requisitos da atividade, a segurança do sistema foi projetada seguindo as melhores práticas de Engenharia de Software:

  1. *Algoritmo Utilizado*
      Foi utilizada a biblioteca cryptography (módulo Fernet), que implementa a criptografia simétrica AES (Advanced Encryption Standard) em modo   CBC, com autenticação de mensagem via HMAC. Isso garante que, se a mensagem for alterada no cabo (ataque de integridade), o servidor detectará e descartará o pacote.
  
  2. *Derivação de Chave (KDF)*
      A chave de 32 bytes necessária para o AES não é armazenada de forma estática no código.
      Em vez disso, utilizamos o protocolo PBKDF2 (Password-Based Key Derivation Function 2):
        - *Senha*: Definida pelo usuário ao iniciar o programa.
        - *Salt*: Utilizamos um "sal" fixo (b'aula_sec') para garantir a derivação correta entre os nós.
        - *Iterações*: 100.000 iterações de hash SHA-256 para dificultar ataques de força bruta e dicionário.

## Requisitos e Instalação:
  **Pré-requisitos:**
    - Python 3.x instalado.
    - Biblioteca de criptografia:
    pip install cryptography
    
  **Como Executar**
    - Inicie o Servidor:
      python servidor.py
    Defina a senha de acesso quando solicitado.
    - Inicie o(s) Cliente(s):
        python cliente.py
    Insira o IP do servidor e a mesma senha definida anteriormente.

## O sistema foi projetado com foco em Cibersegurança:
- *Isolamento de Rede*: Testado em ambiente LAN via conexão direta por cabo Ethernet com
IPs estáticos (192.168.1.1 e 1.2).

- *Tratamento de Exceções*: O servidor gerencia erros de descriptografia (tokens inválidos)
sem interromper o serviço, protegendo a Disponibilidade do sistema.

### Alunos: Allan Victor Vieira, Michel Paula, Thiago Soares
