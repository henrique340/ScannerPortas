import socket
import threading
from queue import Queue

# Constantes
IP_ALVO = "127.0.0.1"
INTERVALO_PORTAS = (1, 1024)
TEMPO_LIMITE = 1  # segundos
NUMERO_THREADS = 100

# Fila para gerenciar o scanner de portas
fila_portas = Queue()
for porta in range(INTERVALO_PORTAS[0], INTERVALO_PORTAS[1] + 1):
  fila_portas.put(porta)

# Lista para armazenar as portas abertas
portas_abertas = []

def escanear_porta(ip_alvo, porta):
  """
  Tenta se conectar a uma porta especifica em um IP alvo

  Args:
    ip_alvo (str): O endereço IP do alvo
    porta (int): A porta que sera verificada

  Returns:
    bool: True se a porta esta aberta, False caso contrario
  """

  try:
    # Cria uma socket TCP e tenta se conectar
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
      sock.settimeout(TEMPO_LIMITE)
      resultado = sock.connect_ex((ip_alvo, porta))
      return resultado == 0
  except Exception as e:
    print(f"Erro ao escanear a porta {porta}: {e}")
    return False
  


def trabalhador(ip_alvo):
  """
  Função executada por cada thread para escanear portas da fila

  Args:
    ip_alvo (str): O endereço IP do alvo
  """

  while not fila_portas.empty():
    porta = fila_portas.get()
    if escanear_porta(ip_alvo, porta):
      print(f"Porta {porta} está aberta!")
      portas_abertas.append(porta)
    fila_portas.task_done()


def executar_scanner(ip_alvo = IP_ALVO):
  """
  Configura as threas e inicia o escaneamento de portas

  Args:
    ip_alvo (str): O endereço IP do alvo
  """

  print(f"Escaneando porta {porta}\n")
  threads = []

  # Cria e inicia threads
  for _ in range(NUMERO_THREADS):
    thread = threading.Thread(target=trabalhador, args=(ip_alvo,))
    thread.start()
    thread.append(thread)

  # Espera todas as threads terminarem
  for thread in threads:
    thread.join()
  
  # Exibe o resultado final
  print("Escaneamento completo!")
  if portas_abertas:
    print("Portas abertas: ", portas_abertas)
  else:
    print("Nenhuma porta aberta foi encontrada")


if __name__ == "__main__":
  # Define o alvo (pode ser substituido por um input do usuário)
  ip_alvo = input("Digite o IP a ser escaneado (padrão: 123.0.0.1): ") or IP_ALVO
  executar_scanner(ip_alvo)
