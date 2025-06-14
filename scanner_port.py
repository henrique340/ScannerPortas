import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

MAX_THREADS = 100
TIMEOUT = 1.0


def scan_single_port(ip: str, port: int, timeout: float = TIMEOUT):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = get_service_name(port)
                banner = get_banner(sock)
                return port, True, service, banner
            return port, False, "", ""
    except Exception:
        return port, False, "", ""


def get_service_name(port: int):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "desconhecido"


def get_banner(sock: socket.socket):
    try:
        return sock.recv(1024).decode(errors="ignore").strip()
    except Exception:
        return ""


def scan_ports_concurrently(ip: str, start_port: int, end_port: int, max_threads: int = MAX_THREADS):
    open_ports = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(scan_single_port, ip, port) for port in range(start_port, end_port + 1)]

        for future in futures:
            port, is_open, service, banner = future.result()
            if is_open:
                open_ports.append((port, service, banner))

    return open_ports


def save_results_to_txt(url: str, ip: str, results: list):
    filename = f"resultado_scan_{url.replace('.', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Alvo: {url} (IP: {ip})\n\n")

        if results:
            f.write("Portas abertas:\n")
            for port, service, _ in results:
                f.write(f" - Porta {port} ({service})\n")

            f.write("\nPortas com banner:\n")
            for port, service, banner in results:
                if banner:
                    f.write(f" - Porta {port} ({service})\n")
                    f.write(f"   ↳ Banner: {banner}\n")
        else:
            f.write("Nenhuma porta aberta encontrada.\n")


def iniciar_scan():
    url = entrada_url.get().strip()
    try:
        ip = socket.gethostbyname(url)
        label_resolucao.config(text=f"{url} → {ip}")
    except socket.gaierror:
        messagebox.showerror("Erro", "Domínio ou IP inválido.")
        return

    try:
        start_port = int(entrada_porta_inicial.get())
        end_port = int(entrada_porta_final.get())
        if not (0 <= start_port <= 65535 and 0 <= end_port <= 65535 and start_port <= end_port):
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Intervalo de portas inválido.")
        return

    texto_resultado.delete("1.0", tk.END)
    texto_resultado.insert(tk.END, f"Iniciando varredura em {url} ({ip}) de {start_port} a {end_port}...\n")
    root.update()

    inicio = datetime.now()
    open_ports = scan_ports_concurrently(ip, start_port, end_port)
    duracao = datetime.now() - inicio

    if open_ports:
        texto_resultado.insert(tk.END, "\nPortas abertas encontradas:\n")
        for port, service, banner in open_ports:
            texto_resultado.insert(tk.END, f" - Porta {port} ({service})\n")
            if banner:
                texto_resultado.insert(tk.END, f"   ↳ Banner: {banner}\n")
    else:
        texto_resultado.insert(tk.END, "\nNenhuma porta aberta encontrada.\n")

    texto_resultado.insert(tk.END, f"\nVarredura finalizada em {duracao}\n")
    save_results_to_txt(url, ip, open_ports)
    messagebox.showinfo("Concluído", "Varredura concluída e resultados salvos em arquivo .txt")


# ---------------- GUI -------------------

root = tk.Tk()
root.title("Scanner de Portas TCP")
root.geometry("720x550")

# IP / Domínio
tk.Label(root, text="Insira o IP ou o domínio:").pack()
entrada_url = tk.Entry(root, width=50)
entrada_url.pack(pady=5)

# Exibição de resolução IP
label_resolucao = tk.Label(root, text="")
label_resolucao.pack()

# Portas
frame_portas = tk.Frame(root)
frame_portas.pack(pady=5)

tk.Label(frame_portas, text="Porta inicial:").grid(row=0, column=0)
entrada_porta_inicial = tk.Entry(frame_portas, width=10)
entrada_porta_inicial.grid(row=0, column=1, padx=5)

tk.Label(frame_portas, text="Porta final:").grid(row=0, column=2)
entrada_porta_final = tk.Entry(frame_portas, width=10)
entrada_porta_final.grid(row=0, column=3, padx=5)

# Botão
btn_scan = tk.Button(root, text="Iniciar varredura", command=iniciar_scan)
btn_scan.pack(pady=10)

# Área de resultado
texto_resultado = scrolledtext.ScrolledText(root, width=85, height=20)
texto_resultado.pack(padx=10, pady=10)

root.mainloop()
