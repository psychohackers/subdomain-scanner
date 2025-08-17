import socket
import concurrent.futures
import argparse

# Colored output (optional)
def print_banner():
    banner = r"""
   ____        _     _                         _____                                      
  / ___| _   _| |__ | | ___  ___ ___  ___     / ____|_ __  _   _ _ __ ___  _ __ ___   ___ 
  \___ \| | | | '_ \| |/ _ \/ __/ __|/ _ \   | |   | '_ \| | | | '__/ _ \| '_ ` _ \ / _ \
   ___) | |_| | |_) | |  __/\__ \__ \ (_) |  | |___| | | | |_| | | | (_) | | | | | |  __/
  |____/ \__,_|_.__/|_|\___||___/___/\___/    \____|_| |_|\__,_|_|  \___/|_| |_| |_|\___|

                    ⚡ Subdomain Scanner Tool - Python 3 ⚡
                            Coded by: [Mr psycho]
                            instagram: [@the_psycho_of_hackers]
    """
    print(banner)

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = ""
        RED = ""
        CYAN = ""
    class Style:
        RESET_ALL = ""

def scan_subdomain(subdomain, domain):
    url = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(url)
        print(f"{Fore.GREEN}[LIVE] {url} -> {ip}")
        return url
    except socket.gaierror:
        print(f"{Fore.RED}[DEAD] {url}")
        return None

def load_wordlist(wordlist_path):
    with open(wordlist_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def main():
    parser = argparse.ArgumentParser(description="Subdomain Scanner in Python")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g. example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to subdomain wordlist")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads (default: 20)")
    args = parser.parse_args()

    subdomains = load_wordlist(args.wordlist)
    found_subdomains = []

    print(f"{Fore.CYAN}[*] Scanning {len(subdomains)} subdomains on {args.domain} with {args.threads} threads...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_subdomain = {executor.submit(scan_subdomain, sub, args.domain): sub for sub in subdomains}
        for future in concurrent.futures.as_completed(future_to_subdomain):
            result = future.result()
            if result:
                found_subdomains.append(result)

    print(f"\n{Fore.CYAN}[+] Scan complete. {len(found_subdomains)} live subdomains found:")
    for sub in found_subdomains:
        print(f"{Fore.GREEN} - {sub}")

if __name__ == "__main__":
    print_banner()
    main()

