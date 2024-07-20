#!/usr/bin/env python3

import speedtest
import argparse
from termcolor import colored
from halo import Halo
import datetime
import os
import csv

LOG_FILE = "speedtest_results.log"
CSV_FILE = "speedtest_results.csv"

def test_speed(test_all=False, test_download=False, test_upload=False, test_ping=False, log=False, server_id=None):
    try:
        st = speedtest.Speedtest()
        spinner = Halo(text='Loading server list', spinner='dots')
        spinner.start()
        st.get_servers()
        if server_id:
            spinner.text = f"Choosing server ID {server_id}"
            st.get_servers([server_id])
            best = st.get_best_server()
        else:
            spinner.text = 'Choosing best server'
            best = st.get_best_server()
        spinner.succeed(colored(f"Connected to: {best['host']} located in {best['country']}", "green"))
        
        results = {}
        results['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if test_all or test_download:
            spinner.start(text='Testing download speed...')
            download_speed = st.download()
            spinner.succeed(colored(f"Download speed: {download_speed / 1_000_000:.2f} Mbps", "cyan"))
            results['download'] = download_speed / 1_000_000
        
        if test_all or test_upload:
            spinner.start(text='Testing upload speed...')
            upload_speed = st.upload()
            spinner.succeed(colored(f"Upload speed: {upload_speed / 1_000_000:.2f} Mbps", "cyan"))
            results['upload'] = upload_speed / 1_000_000
        
        if test_all or test_ping:
            spinner.start(text='Ping test...')
            ping_result = st.results.ping
            spinner.succeed(colored(f"Ping: {ping_result} ms", "cyan"))
            results['ping'] = ping_result

        public_ip = st.results.share()
        print(colored(f"Public IP address: {public_ip}", "blue"))
        results['public_ip'] = public_ip

        if log:
            with open(LOG_FILE, "a") as log_file:
                log_file.write(f"{results}\n")
            with open(CSV_FILE, "a", newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=results.keys())
                if os.stat(CSV_FILE).st_size == 0:
                    writer.writeheader()
                writer.writerow(results)
            print(colored(f"Results logged to {LOG_FILE} and {CSV_FILE}", "yellow"))
    
    except speedtest.ConfigRetrievalError:
        spinner.fail(colored("Failed to retrieve configuration from Speedtest.net", "red"))
    except speedtest.NoMatchedServers:
        spinner.fail(colored("No matched servers found. Try a different server ID.", "red"))
    except speedtest.SpeedtestBestServerFailure:
        spinner.fail(colored("Failed to find the best server.", "red"))
    except speedtest.SpeedtestServersRetrievalError:
        spinner.fail(colored("Failed to retrieve the server list from Speedtest.net", "red"))
    except Exception as e:
        spinner.fail(colored(f"An error occurred: {e}", "red"))

def display_logs(entries):
    try:
        with open(LOG_FILE, "r") as log_file:
            lines = log_file.readlines()
            if entries > 0:
                lines = lines[-entries:]
            for line in lines:
                print(line.strip())
    except FileNotFoundError:
        print(colored("No log file found. Run a speed test first.", "red"))

def clear_logs():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print(colored("Log file cleared.", "yellow"))
    else:
        print(colored("No log file found to clear.", "red"))
    
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
        print(colored("CSV file cleared.", "yellow"))
    else:
        print(colored("No CSV file found to clear.", "red"))

def display_summary():
    try:
        with open(CSV_FILE, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            summary = {
                "total_tests": 0,
                "total_download": 0,
                "total_upload": 0,
                "total_ping": 0
            }
            for row in reader:
                summary["total_tests"] += 1
                summary["total_download"] += float(row.get("download", 0))
                summary["total_upload"] += float(row.get("upload", 0))
                summary["total_ping"] += float(row.get("ping", 0))
            if summary["total_tests"] > 0:
                summary["avg_download"] = summary["total_download"] / summary["total_tests"]
                summary["avg_upload"] = summary["total_upload"] / summary["total_tests"]
                summary["avg_ping"] = summary["total_ping"] / summary["total_tests"]
            else:
                summary["avg_download"] = summary["avg_upload"] = summary["avg_ping"] = 0
            
            print(colored(f"Total tests performed: {summary['total_tests']}", "green"))
            print(colored(f"Average download speed: {summary['avg_download']:.2f} Mbps", "cyan"))
            print(colored(f"Average upload speed: {summary['avg_upload']:.2f} Mbps", "cyan"))
            print(colored(f"Average ping: {summary['avg_ping']:.2f} ms", "cyan"))
    except FileNotFoundError:
        print(colored("No CSV file found. Run a speed test first.", "red"))

def main():
    parser = argparse.ArgumentParser(description="speedPy: Internet Speed Test", add_help=False)
    parser.add_argument('--all', action='store_true', help="Test download, upload, and ping speeds")
    parser.add_argument('--download', action='store_true', help="Test download speed")
    parser.add_argument('--upload', action='store_true', help="Test upload speed")
    parser.add_argument('--ping', action='store_true', help="Test ping")
    parser.add_argument('--log', action='store_true', help="Log results to a file")
    parser.add_argument('--show-ip', action='store_true', help="Show public IP address")
    parser.add_argument('--logs', type=int, metavar='N', help="Display the last N log entries")
    parser.add_argument('--clear-logs', action='store_true', help="Clear the log file")
    parser.add_argument('--summary', action='store_true', help="Show summary of all tests performed")
    parser.add_argument('--server', type=int, metavar='ID', help="Use a specific server ID for testing")
    parser.add_argument('--version', action='version', version='speedPy 1.0')
    parser.add_argument('--help', action='store_true', help="Show this help message and exit")
    args = parser.parse_args()

    if args.help or not any(vars(args).values()):
        parser.print_help()
    elif args.logs:
        display_logs(args.logs)
    elif args.clear_logs:
        clear_logs()
    elif args.summary:
        display_summary()
    else:
        test_speed(test_all=args.all, test_download=args.download, test_upload=args.upload, test_ping=args.ping, log=args.log, server_id=args.server)

if __name__ == "__main__":
    main()
