#  Scanner de Portas TCP com Interface Gráfica

Este projeto é um scanner de portas TCP simples, desenvolvido em Python com interface gráfica usando a biblioteca `tkinter`. Ele permite ao usuário inserir um domínio ou IP, especificar um intervalo de portas, e realizar a varredura de forma concorrente. As portas abertas são exibidas com informações adicionais, como o serviço padrão e o banner, se disponível. Os resultados são salvos automaticamente em um arquivo `.txt`.

---

##  Requisitos e Como Executar

###  Instalação
Certifique-se de ter o Python 3 instalado.

Você também pode (opcionalmente) criar um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate.bat  # Windows
```

###  Como Executar o Programa

1. **Certifique-se de ter o Python 3 instalado.**

2. **Instale os módulos necessários:**
   
   Este projeto usa apenas bibliotecas da biblioteca padrão do Python, então não é necessário instalar pacotes externos.

3. **Execute o programa:**

   ```bash
   python scanner_gui.py
   ```

---

##  Funcionalidades Utilizadas

### Bibliotecas
- `socket`: comunicação de rede (sockets, resolução de IP, banners).
- `tkinter`: construção da interface gráfica.
- `concurrent.futures.ThreadPoolExecutor`: execução paralela da varredura de portas.
- `datetime`: medir a duração da varredura.
- `tkinter.scrolledtext`: caixa de texto com rolagem para exibir os resultados.

### Funções e Componentes
- `scan_single_port()`: escaneia uma porta específica e tenta capturar o banner.
- `scan_ports_concurrently()`: escaneia múltiplas portas usando threads.
- `get_service_name()`: retorna o nome do serviço associado à porta (ex: HTTP, FTP).
- `get_banner()`: captura a mensagem inicial (banner) enviada pelo serviço, se disponível.
- `save_results_to_txt()`: salva o resultado em um arquivo `.txt` automaticamente.
- Interface com `tk.Entry`, `tk.Button`, `tk.Label`, e `tkinter.scrolledtext`.

Todas essas funções foram integradas para criar um scanner funcional e visualmente simples com o mínimo de dependências externas.

