#!/usr/bin/env python3

import platform
import psutil
import datetime
import time
import socket
import distro
import subprocess
from halo import Halo
from pyfiglet import Figlet

# Define ANSI escape codes for pastel colors
PASTEL_CYAN = '\033[38;2;173;216;230m'
PASTEL_GREEN = '\033[38;2;144;238;144m'
RESET = '\033[0m'

def get_system_info():
    info = {
        'OS': distro.name(pretty=True),
        'OS Version': distro.version(),
        'Architecture': platform.machine(),
        'Hostname': platform.node(),
        'Kernel': platform.release(),
        'Uptime': get_uptime(),
        'CPU': get_cpu_info(),
        'Memory': get_memory_info(),
        'Disk': get_disk_info(),
        'GPU': get_gpu_info(),
        'IP Address': get_ip_address()
    }
    return info

def get_uptime():
    uptime_seconds = int(time.time() - psutil.boot_time())
    uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
    return uptime_str

def get_cpu_info():
    return f"{platform.processor()} ({psutil.cpu_count(logical=True)} cores)"

def get_memory_info():
    memory = psutil.virtual_memory()
    return f"{memory.total // (1024 ** 3)} GB"

def get_disk_info():
    disk = psutil.disk_usage('/')
    return f"{disk.total // (1024 ** 3)} GB"

def get_gpu_info():
    try:
        lspci_output = subprocess.check_output("lspci | grep -i 'vga\\|3d\\|2d'", shell=True, text=True)
        gpus = lspci_output.strip().split('\n')
        return '\n            '.join(gpus)  # Indent subsequent lines
    except subprocess.CalledProcessError:
        return 'N/A'

def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        return 'N/A'

def display_info(info):
    f = Figlet(font='slant')
    figlet_text = f.renderText('Qirky')
    print(PASTEL_CYAN + figlet_text + RESET)

    max_key_length = max(len(key) for key in info.keys())
    for key, value in info.items():
        if '\n' in value:
            print(f'{PASTEL_GREEN}{key.ljust(max_key_length)}:{RESET} {PASTEL_CYAN}{value.splitlines()[0]}{RESET}')
            for line in value.splitlines()[1:]:
                print(f'{" " * (max_key_length + 2)} {PASTEL_CYAN}{line}{RESET}')
        else:
            print(f'{PASTEL_GREEN}{key.ljust(max_key_length)}:{RESET} {PASTEL_CYAN}{value}{RESET}')

def main():
    spinner = Halo(text='Gathering system information', spinner='dots')
    spinner.start()
    try:
        system_info = get_system_info()
        spinner.stop()
        display_info(system_info)
    except Exception as e:
        spinner.fail(PASTEL_GREEN + f"An error occurred: {e}" + RESET)

if __name__ == "__main__":
    main()
