#!/usr/bin/env python3
"""
Subdomain Scanner Tool
A powerful subdomain enumeration tool using DNS resolution and multithreading.
"""

import socket
import concurrent.futures
import argparse
import sys

def print_banner():
    """Display the tool banner"""
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

# Try to import colorama for colored output
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS_ENABLED = True
except ImportError:
    # Fallback if colorama is not installed
    class Fore:
        GREEN = ""
        RED = ""
        CYAN = ""
        YELLOW = ""
    class Style:
        RESET_ALL = ""
    COLORS_ENABLED = False

def scan_subdomain(subdomain, domain):
    """
    Scan a single subdomain to check if it exists.
    
    Args:
        subdomain (str): The subdomain prefix to check
        domain (str): The target domain
        
    Returns:
        str or None: The full subdomain URL if live, None if dead
    """
    url = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(url)
        print(f"{Fore.GREEN}[LIVE] {url} -> {ip}")
        return url
    except socket.gaierror:
        print(f"{Fore.RED}[DEAD] {url}")
        return None

def load_wordlist(wordlist_path):
    """
    Load subdomain wordlist from file.
    
    Args:
        wordlist_path (str): Path to the wordlist file
        
    Returns:
        list: List of subdomain names
    """
    try:
        with open(wordlist_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR] Wordlist file not found: {wordlist_path}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Failed to read wordlist: {e}")
        sys.exit(1)

def save_results(output_file, subdomains):
    """
    Save live subdomains to output file.
    
    Args:
        output_file (str): Path to the output file
        subdomains (list): List of live subdomains to save
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for sub in subdomains:
                f.write(sub + "\n")
        print(f"\n{Fore.CYAN}[+] Live subdomains saved to: {output_file}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to write output file: {e}")

def main():
    """Main function to run the subdomain scanner"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Subdomain Scanner - Discover subdomains using DNS resolution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python subdomain.py -d example.com -w wordlist.txt
  python subdomain.py -d example.com -w wordlist.txt -t 50
  python subdomain.py -d example.com -w wordlist.txt -o results.txt
        """
    )
    
    parser.add_argument(
        "-d", "--domain", 
        required=True, 
        help="Target domain (e.g., example.com)"
    )
    parser.add_argument(
        "-w", "--wordlist", 
        required=True, 
        help="Path to subdomain wordlist file"
    )
    parser.add_argument(
        "-t", "--threads", 
        type=int, 
        default=20, 
        help="Number of concurrent threads (default: 20)"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Output file to save live subdomains (optional)"
    )
    
    args = parser.parse_args()

    # Load wordlist
    subdomains = load_wordlist(args.wordlist)
    found_subdomains = []

    print(f"{Fore.CYAN}[*] Scanning {len(subdomains)} subdomains on {args.domain} with {args.threads} threads...\n")

    # Scan subdomains using multithreading
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_subdomain = {
            executor.submit(scan_subdomain, sub, args.domain): sub 
            for sub in subdomains
        }
        
        for future in concurrent.futures.as_completed(future_to_subdomain):
            result = future.result()
            if result:
                found_subdomains.append(result)

    # Display results
    print(f"\n{Fore.CYAN}[+] Scan complete. {len(found_subdomains)} live subdomains found:")
    for sub in found_subdomains:
        print(f"{Fore.GREEN} - {sub}")

    # Save to output file if requested
    if args.output:
        save_results(args.output, found_subdomains)
    
    print(f"\n{Fore.CYAN}[+] Scan finished successfully!")

if __name__ == "__main__":
    print_banner()
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Scan interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] An unexpected error occurred: {e}")
        sys.exit(1)

