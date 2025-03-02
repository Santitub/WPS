import requests
import argparse
import time
import signal
import sys
from random import uniform
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

BANNER = f"""{Fore.CYAN}{Style.BRIGHT}
    ██╗    ██╗██████╗ ███████╗
    ██║    ██║██╔══██╗██╔════╝
    ██║ █╗ ██║██████╔╝███████╗
    ██║███╗██║██╔═══╝ ╚════██║
    ╚███╔███╔╝██║     ███████║
     ╚══╝╚══╝ ╚═╝     ╚══════╝
    
  WordPress Plugins Scanner
{Style.RESET_ALL}"""

shutdown = False

def handle_sigint(signal, frame):
    global shutdown
    if not shutdown:
        shutdown = True
        print(f"\n{Fore.RED}[!]{Style.RESET_ALL} Finalizando de forma segura...")
        sys.exit(1)

def check_plugin(target_url, plugin, timeout=15):
    if shutdown:
        return (None, None, None)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url = f"{target_url.rstrip('/')}/wp-content/plugins/{plugin}/"
    
    try:
        time.sleep(uniform(0.01, 0.05))
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=False)
        
        if response.status_code == 200:
            return ("found", plugin, url)
        elif response.status_code == 403:
            readme_url = f"{url}readme.txt"
            readme_response = requests.head(readme_url, headers=headers, timeout=timeout)
            if readme_response.status_code == 200:
                return ("found", plugin, url)
            return ("possible", plugin, url)
            
    except requests.exceptions.RequestException:
        return (None, None, None)
    
    return (None, None, None)

def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description='Detector de plugins de WordPress')
    parser.add_argument('-u', '--url', required=True, help='URL objetivo')
    parser.add_argument('-w', '--wordlist', required=True, help='Ruta a la wordlist')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Número de hilos (1-50)')
    parser.add_argument('-to', '--timeout', type=int, default=15, help='Timeout por petición')
    args = parser.parse_args()

    args.threads = max(1, min(50, args.threads))
    args.timeout = max(5, min(30, args.timeout))

    print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Escaneando: {args.url}")
    print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Hilos: {args.threads}")
    print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Timeout: {args.timeout}s\n")

    try:
        with open(args.wordlist, 'r', errors='ignore') as f:
            plugins = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Error: Wordlist no encontrada{Style.RESET_ALL}")
        return

    total_plugins = len(plugins)
    found = []
    possible = []

    try:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = {executor.submit(check_plugin, args.url, plugin, args.timeout): plugin for plugin in plugins}
            
            # Barra de progreso modificada
            with tqdm(
                total=total_plugins, 
                desc="Progreso", 
                unit="plugin", 
                position=0,
                leave=True,
                dynamic_ncols=True,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
            ) as pbar:
                try:
                    for future in as_completed(futures):
                        if shutdown:
                            executor.shutdown(wait=False, cancel_futures=True)
                            pbar.close()
                            break
                        
                        result_type, plugin, extra = future.result()
                        
                        if result_type == "found":
                            found.append(plugin)
                            tqdm.write(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} Encontrado: {Fore.CYAN}{plugin}{Style.RESET_ALL} ({extra})")
                        elif result_type == "possible":
                            possible.append(plugin)
                            tqdm.write(f"\n{Fore.YELLOW}[!]{Style.RESET_ALL} Posible (403): {plugin}")
                        
                        pbar.update(1)
                except KeyboardInterrupt:
                    executor.shutdown(wait=False, cancel_futures=True)
                    pbar.close()
                    sys.exit(1)
                    
    except Exception as e:
        print(f"{Fore.RED}[!] Error crítico: {e}{Style.RESET_ALL}")
        sys.exit(1)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}[*] Escaneo completado!")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Plugins probados: {total_plugins}")
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Confirmados: {len(found)}")
    print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} Posibles: {len(possible)}")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_sigint)
    main()