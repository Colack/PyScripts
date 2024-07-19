#!/usr/bin/env python3

import speedtest
import argparse
from termcolor import colored

def test_speed(test_all=False, test_download=False, test_upload=False, test_ping=False):
    try:
        st = speedtest.Speedtest()
        print(colored("Loading server list...", "yellow"))
        st.get_servers()
        print(colored("Choosing best server...", "yellow"))
        best = st.get_best_server()
        print(colored(f"Connected to: {best['host']} located in {best['country']}", "green"))
        
        if test_all or test_download:
            print(colored("Testing download speed...", "yellow"))
            download_speed = st.download()
            print(colored(f"Download speed: {download_speed / 1_000_000:.2f} Mbps", "cyan"))
        
        if test_all or test_upload:
            print(colored("Testing upload speed...", "yellow"))
            upload_speed = st.upload()
            print(colored(f"Upload speed: {upload_speed / 1_000_000:.2f} Mbps", "cyan"))
        
        if test_all or test_ping:
            print(colored("Ping test...", "yellow"))
            ping_result = st.results.ping
            print(colored(f"Ping: {ping_result} ms", "cyan"))
    
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))

def main():
    parser = argparse.ArgumentParser(description="speedPy: Internet Speed Test", add_help=False)
    parser.add_argument('--all', action='store_true', help="Test download, upload, and ping speeds")
    parser.add_argument('--download', action='store_true', help="Test download speed")
    parser.add_argument('--upload', action='store_true', help="Test upload speed")
    parser.add_argument('--ping', action='store_true', help="Test ping")
    parser.add_argument('--version', action='version', version='speedPy 1.0')
    parser.add_argument('--help', action='store_true', help="Show this help message and exit")
    args = parser.parse_args()

    if args.help or not any(vars(args).values()):
        parser.print_help()
    else:
        test_speed(test_all=args.all, test_download=args.download, test_upload=args.upload, test_ping=args.ping)

if __name__ == "__main__":
    main()
