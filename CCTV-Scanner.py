#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IP Range Camera Scanner
Author: ipxo
Telegram:@ipxo_bd_back
Description: Scan custom IP ranges for cameras
License: MIT
Termux Compatible: Yes
"""

import socket
import threading
from queue import Queue
import ipaddress
from datetime import datetime
import time
import sys
import signal
import os
import re
import multiprocessing
import subprocess
import platform

# Try to import colorama, but work without it (Termux compatibility)
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Fallback color codes
    class Fore:
        GREEN = '\033[92m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
    
    class Style:
        RESET_ALL = '\033[0m'

# Configuration
CCTV_OUTPUT = "CCTV_Found.txt"

# Set a default timeout for socket connections
socket.setdefaulttimeout(0.25)

# Set to store detected IPs
detected_ips = set()

# Global control flags
stop_scan = False
pause_scan = False


def print_banner():
    """Display main banner"""
    banner = f"""
██╗██████╗ ██╗  ██╗ ██████╗ 
██║██╔══██╗╚██╗██╔╝██╔═══██╗
██║██████╔╝ ╚███╔╝ ██║   ██║
██║██╔═══╝  ██╔██╗ ██║   ██║
██║██║     ██╔╝ ██╗╚██████╔╝
╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
                            

"""
    print(f"{Fore.RED}{banner}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Developed by: {Fore.YELLOW}ipxo{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Telegram: {Fore.YELLOW}@ipxo_bd_back{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Termux Supported ✓{Style.RESET_ALL}\n")


def validate_ip(ip_str):
    """Validate IP address format"""
    try:
        ipaddress.IPv4Address(ip_str)
        return True
    except:
        return False


def get_default_gateway():
    """Get the default gateway (router) IP address"""
    try:
        system = platform.system()
        
        if system == "Windows":
            # Windows command
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            output = result.stdout
            
            # Look for Default Gateway
            for line in output.split('\n'):
                if 'Default Gateway' in line or 'Default Gateway' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        gateway = parts[1].strip()
                        if gateway and gateway != '' and validate_ip(gateway):
                            return gateway
        
        elif system == "Linux" or system == "Darwin":  # Linux or macOS
            # Unix/Linux/Mac command
            result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            output = result.stdout
            
            # Look for default route
            for line in output.split('\n'):
                if 'default' in line:
                    parts = line.split()
                    if len(parts) > 2:
                        gateway = parts[2]
                        if validate_ip(gateway):
                            return gateway
            
            # Fallback for macOS
            result = subprocess.run(['route', '-n', 'get', 'default'], capture_output=True, text=True)
            output = result.stdout
            for line in output.split('\n'):
                if 'gateway:' in line:
                    gateway = line.split(':')[1].strip()
                    if validate_ip(gateway):
                        return gateway
        
        return "Not Found"
    except:
        return "Not Found"


def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Not Found"


def extract_title(html_content):
    """Extract title from HTML content"""
    try:
        match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return "No Title Found"
    except:
        return "Error Extracting Title"


def trace_route():
    """Trace route to a domain/IP"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[🔍] TRACE ROUTE MODE [🔍]{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    # Automatically use google.com as target
    target = "google.com"
    
    print(f"{Fore.GREEN}[i] Target: {Fore.CYAN}{target}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Tracing route to {Fore.CYAN}{target}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Please wait...{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}{'─'*50}{Style.RESET_ALL}\n")
    
    try:
        system = platform.system()
        
        if system == "Windows":
            # Windows tracert command (fast mode with max 30 hops)
            cmd = ['tracert', '-d', '-h', '30', '-w', '1000', target]
        else:
            # Linux/macOS/Termux traceroute command
            # Try multiple commands in order of preference
            cmd = None
            
            # Try traceroute first
            try:
                result = subprocess.run(['traceroute', '--version'], capture_output=True, timeout=2)
                cmd = ['traceroute', '-n', '-m', '30', '-w', '1', target]
            except:
                pass
            
            # Try tracepath as fallback
            if cmd is None:
                try:
                    result = subprocess.run(['tracepath', '-V'], capture_output=True, timeout=2)
                    cmd = ['tracepath', '-n', target]
                except:
                    pass
            
            # If nothing works, default to traceroute (will show error if not found)
            if cmd is None:
                cmd = ['traceroute', '-n', '-m', '30', '-w', '1', target]
        
        # Run the command and display output in real-time
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        hop_count = 0
        for line in iter(process.stdout.readline, ''):
            if line:
                line = line.strip()
                
                # Color code the output
                if '*' in line or 'timeout' in line.lower():
                    print(f"{Fore.RED}{line}{Style.RESET_ALL}")
                elif 'ms' in line.lower() or 'Tracing' in line or 'traceroute' in line:
                    # Highlight successful hops
                    if any(char.isdigit() for char in line) and ('ms' in line.lower() or '<' in line):
                        hop_count += 1
                        print(f"{Fore.GREEN}[Hop {hop_count:2d}] {line}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.CYAN}{line}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.WHITE}{line}{Style.RESET_ALL}")
        
        process.wait()
        
        print(f"\n{Fore.CYAN}{'─'*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Trace complete!{Style.RESET_ALL}")
        
        if hop_count > 0:
            print(f"{Fore.CYAN}[i] Total hops: {hop_count}{Style.RESET_ALL}")
        
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Traceroute command not found on this system{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[i] For Termux, install: pkg install inetutils{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[i] Or install: pkg install traceroute{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")


def super_fast_scan():
    """Super fast scan with full threading power"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.RED}[⚡] SUPER FAST SCAN MODE [⚡]{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}[i] Maximum performance mode enabled{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[i] Uses multi-threading for ultra-fast scanning{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}Examples:{Style.RESET_ALL}")
    print(f"  Single IP: 192.168.1.1")
    print(f"  IP Range: 192.168.1.1 to 192.168.1.255\n")
    
    # Get start IP
    while True:
        start_ip = input(f"{Fore.GREEN}Enter Start IP: {Style.RESET_ALL}").strip()
        if not validate_ip(start_ip):
            print(f"{Fore.RED}[!] Invalid IP address format!{Style.RESET_ALL}")
            continue
        break
    
    # Get end IP (optional)
    end_ip = input(f"{Fore.GREEN}Enter End IP (press Enter for single IP): {Style.RESET_ALL}").strip()
    
    # Generate IP list
    ip_list = []
    if not end_ip:
        ip_list = [start_ip]
    else:
        if not validate_ip(end_ip):
            print(f"{Fore.RED}[!] Invalid End IP! Scanning single IP only.{Style.RESET_ALL}")
            ip_list = [start_ip]
        else:
            start_int = int(ipaddress.IPv4Address(start_ip))
            end_int = int(ipaddress.IPv4Address(end_ip))
            
            if start_int > end_int:
                print(f"{Fore.RED}[!] Start IP must be less than End IP!{Style.RESET_ALL}")
                ip_list = [start_ip]
            else:
                for ip_int in range(start_int, end_int + 1):
                    ip_list.append(str(ipaddress.IPv4Address(ip_int)))
    
    print(f"\n{Fore.GREEN}[✓] Total IPs to scan: {len(ip_list)}{Style.RESET_ALL}")
    
    # Auto-detect optimal thread count
    cpu_count = multiprocessing.cpu_count()
    max_threads = min(500, cpu_count * 50)  # Scale with CPU cores
    
    print(f"{Fore.CYAN}[i] CPU Cores: {cpu_count}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Threads: {max_threads}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Starting super fast scan...{Style.RESET_ALL}\n")
    
    ports = [80, 8080]
    results = []
    results_lock = threading.Lock()
    scan_queue = Queue()
    
    # Worker function for threading
    def worker():
        while True:
            try:
                ip, port = scan_queue.get(timeout=0.5)
                
                try:
                    # Ultra-fast port check
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)  # Super fast timeout
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    
                    if result == 0:
                        # Port is open, get HTTP data
                        try:
                            http_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            http_sock.settimeout(1)
                            http_sock.connect((ip, port))
                            
                            request = f'GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n'
                            http_sock.send(request.encode())
                            
                            response = b''
                            http_sock.settimeout(2)
                            while True:
                                try:
                                    data = http_sock.recv(4096)
                                    if not data:
                                        break
                                    response += data
                                    if len(response) > 30000:
                                        break
                                except:
                                    break
                            
                            http_sock.close()
                            
                            if response:
                                response_str = response.decode('utf-8', errors='ignore')
                                title = extract_title(response_str)
                                
                                # Server header
                                server_match = re.search(r'Server: ([^\r\n]+)', response_str, re.IGNORECASE)
                                server = server_match.group(1) if server_match else "Unknown"
                                
                                url = f"http://{ip}:{port}" if port != 80 else f"http://{ip}"
                                
                                # Detect camera type based on title and content
                                camera_type = None
                                title_lower = title.lower()
                                
                                if 'web service' in title_lower or '<title>WEB SERVICE</title>' in response_str:
                                    camera_type = "Camera - WEB SERVICE"
                                elif 'web' in title_lower:
                                    camera_type = "Camera - WEB"
                                elif 'login' in title_lower:
                                    camera_type = "Camera - Login"
                                elif 'login.asp' in response_str:
                                    camera_type = "Camera - HIK Vision"
                                elif 'dvr' in title_lower or 'camera' in title_lower:
                                    camera_type = "Camera - DVR"
                                elif 'ipcam' in title_lower or 'ip cam' in title_lower:
                                    camera_type = "Camera - IP Camera"
                                
                                # Only save and display if it's a camera (not regular web server)
                                if camera_type:
                                    with results_lock:
                                        results.append({
                                            'ip': ip,
                                            'port': port,
                                            'title': title,
                                            'server': server,
                                            'url': url,
                                            'type': camera_type
                                        })
                                        print(f"{Fore.GREEN}[✓] Camera Found: {ip}:{port} - {title[:40]}{Style.RESET_ALL}")
                        except:
                            pass
                except:
                    pass
                
                scan_queue.task_done()
            except:
                break
    
    # Start threads
    threads = []
    for _ in range(max_threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)
    
    # Queue all IP:port combinations
    start_time = time.time()
    for ip in ip_list:
        for port in ports:
            scan_queue.put((ip, port))
    
    # Wait for completion
    scan_queue.join()
    elapsed = time.time() - start_time
    
    # Display results
    print(f"\n{Fore.CYAN}{'═'*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[✓] SUPER FAST SCAN COMPLETE!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═'*50}{Style.RESET_ALL}\n")
    
    if results:
        print(f"{Fore.RED}[*] Found {len(results)} CAMERAS:{Style.RESET_ALL}\n")
        for idx, r in enumerate(results, 1):
            print(f"{Fore.CYAN}[{idx}] {r['ip']}:{r['port']}{Style.RESET_ALL}")
            print(f"    Title: {Fore.YELLOW}{r['title']}{Style.RESET_ALL}")
            print(f"    Server: {Fore.YELLOW}{r['server']}{Style.RESET_ALL}")
            print(f"    Type: {Fore.RED}{r['type']}{Style.RESET_ALL}")
            print(f"    URL: {Fore.WHITE}{r['url']}{Style.RESET_ALL}")
            print()
        
        # Save to file
        try:
            with open("SuperFastScan_Results.txt", 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("SUPER FAST SCAN - CAMERAS FOUND\n")
                f.write("="*60 + "\n\n")
                for r in results:
                    f.write(f"IP: {r['ip']}:{r['port']}\n")
                    f.write(f"Title: {r['title']}\n")
                    f.write(f"Server: {r['server']}\n")
                    f.write(f"Type: {r['type']}\n")
                    f.write(f"URL: {r['url']}\n")
                    f.write("-"*60 + "\n\n")
            print(f"{Fore.GREEN}[✓] Results saved to: SuperFastScan_Results.txt{Style.RESET_ALL}")
        except:
            pass
    else:
        print(f"{Fore.YELLOW}[!] No cameras found{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}[i] Total IPs scanned: {len(ip_list)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Cameras found: {len(results)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Time taken: {elapsed:.2f} seconds{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Speed: {(len(ip_list)*2)/elapsed:.0f} ports/sec{Style.RESET_ALL}")


def scan(ip, port):
    """Scan a specific IP and port for cameras"""
    global stop_scan, pause_scan
    
    # Check if scan should stop
    if stop_scan:
        return
    
    # Wait while paused
    while pause_scan and not stop_scan:
        time.sleep(0.1)
    
    if stop_scan:
        return
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.send(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
            response = sock.recv(4096).decode()
            
            camera_found = False
            camera_type = ""
            url = f"http://{ip}:{port}" if port == 8080 else f"http://{ip}"
            
            if 'HTTP' in response and '<title>WEB SERVICE</title>' in response:
                if ip not in detected_ips:
                    detected_ips.add(ip)
                    camera_type = "Anjhua-Dahua Technology Camera"
                    camera_found = True
                    print(f"{Fore.GREEN}[✓] {camera_type} Found!{Style.RESET_ALL} at {Fore.CYAN}{url}{Style.RESET_ALL}")
                    
            elif 'HTTP' in response and 'login.asp' in response:
                if ip not in detected_ips:
                    detected_ips.add(ip)
                    camera_type = "HIK Vision Camera"
                    camera_found = True
                    print(f"{Fore.RED}[✓] {camera_type} Found!{Style.RESET_ALL} at {Fore.CYAN}{url}{Style.RESET_ALL}")
            
            # Live save to file
            if camera_found:
                try:
                    with open(CCTV_OUTPUT, 'a', encoding='utf-8') as file:
                        file.write(f"{'='*60}\n")
                        file.write(f"Camera Type: {camera_type}\n")
                        file.write(f"IP Address: {ip}\n")
                        file.write(f"Port: {port}\n")
                        file.write(f"URL: {url}\n")
                        file.write(f"Detection Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        file.write(f"{'='*60}\n\n")
                        file.flush()  # Force write to disk immediately (live save)
                except Exception as e:
                    pass
                    
    except Exception as e:
        pass


def execute(queue):
    """Execute the scan from the queue"""
    global stop_scan
    try:
        while not stop_scan:
            try:
                ip, port = queue.get(timeout=0.5)
                scan(ip, port)
                queue.task_done()
            except:
                if stop_scan:
                    break
                continue
    except KeyboardInterrupt:
        stop_scan = True
        return


def signal_handler_stop(signum, frame):
    """Handle Ctrl+C - Immediate stop"""
    global stop_scan
    stop_scan = True
    print(f"\n\n{Fore.RED}[!] Ctrl+C detected - STOPPING IMMEDIATELY...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Cleaning up threads...{Style.RESET_ALL}")
    sys.exit(0)


def signal_handler_pause(signum, frame):
    """Handle Ctrl+Z - Pause/Resume"""
    global pause_scan
    pause_scan = not pause_scan
    if pause_scan:
        print(f"\n\n{Fore.YELLOW}[⏸] SCAN PAUSED - Press Ctrl+Z again to resume...{Style.RESET_ALL}\n")
    else:
        print(f"\n\n{Fore.GREEN}[▶] SCAN RESUMED - Continuing...{Style.RESET_ALL}\n")


def run_scanner(ip_list):
    """Run the IP scanner"""
    global stop_scan, pause_scan
    
    # Reset flags
    stop_scan = False
    pause_scan = False
    
    # Register signal handlers
    try:
        signal.signal(signal.SIGINT, signal_handler_stop)  # Ctrl+C
        if hasattr(signal, 'SIGTSTP'):  # Unix/Linux/Mac
            signal.signal(signal.SIGTSTP, signal_handler_pause)  # Ctrl+Z
    except:
        pass  # Windows might not support SIGTSTP
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Starting Camera Scanner{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}[*] Controls:{Style.RESET_ALL}")
    print(f"  {Fore.RED}Ctrl+C{Style.RESET_ALL} - Stop scan immediately")
    if hasattr(signal, 'SIGTSTP'):
        print(f"  {Fore.YELLOW}Ctrl+Z{Style.RESET_ALL} - Pause/Resume scan")
    print()
    
    print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Starting scan on ports 80 and 8080...")
    print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Results will be saved to {Fore.GREEN}{CCTV_OUTPUT}{Style.RESET_ALL} (Live Save)\n")
    
    queue = Queue()
    start_time = time.time()
    
    # Create worker threads
    threads = []
    for _ in range(100):
        thread = threading.Thread(target=execute, args=(queue,), daemon=True)
        thread.start()
        threads.append(thread)
    
    # Enqueue IPs and ports for scanning
    try:
        total_ips = 0
        for ip in ip_list:
                if stop_scan:
                    break
                queue.put((ip, 80))
                queue.put((ip, 8080))
                total_ips += 1
        
        if not stop_scan:
            print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} Queued {total_ips} IPs for scanning")
            print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Scanning in progress...\n")
            
            # Wait for all tasks to complete or stop signal
            while not stop_scan and not queue.empty():
                time.sleep(0.5)
        
    except KeyboardInterrupt:
        stop_scan = True
        print(f"\n\n{Fore.YELLOW}[!]{Style.RESET_ALL} Ctrl+C detected. Stopping...")
    except Exception as e:
        print(f"\n{Fore.RED}[!]{Style.RESET_ALL} Error: {e}")
    
    # Mark as stopped
    stop_scan = True
    time.sleep(1)  # Give threads time to finish
    
    elapsed_time = time.time() - start_time
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[✓] Scan Complete!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Time taken: {elapsed_time:.2f} seconds")
    print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Cameras found: {len(detected_ips)}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")


def get_subnet():
    """Get local subnet"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ".".join(ip.split(".")[:3])
    except:
        return None


def is_rtsp(ip):
    """Check if RTSP port 554 is open"""
    try:
        s = socket.socket()
        s.settimeout(0.3)
        ok = s.connect_ex((ip, 554)) == 0
        s.close()
        return ok
    except:
        return False


def dahua_name(ip):
    """Get Dahua camera name"""
    try:
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((ip, 37777))
        data = s.recv(512).decode(errors="ignore")
        s.close()
        
        m = re.search(r"DH-[A-Z0-9\-]+", data)
        if m:
            return m.group(0)
    except:
        pass
    return None


def hikvision_name(ip):
    """Get Hikvision camera name"""
    try:
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((ip, 8000))
        data = s.recv(512).decode(errors="ignore")
        s.close()
        
        if "Hikvision" in data:
            return "HIKVISION CAMERA"
    except:
        pass
    return None


def scan_rtsp_ip(ip, results, results_lock):
    """Scan single IP for RTSP camera"""
    if not is_rtsp(ip):
        return
    
    name = (
        dahua_name(ip)
        or hikvision_name(ip)
        or "RTSP CAMERA"
    )
    
    with results_lock:
        results.append({
            'ip': ip,
            'name': name,
            'rtsp_url': f"rtsp://{ip}:554"
        })
        print(f"{Fore.GREEN}[✓] Camera Found: {ip} - {name}{Style.RESET_ALL}")


def neighbours_camera_scanner():
    """Scan local network for RTSP cameras"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[📷] NEIGHBOURS CAMERA SCANNER [📷]{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    subnet = get_subnet()
    if not subnet:
        print(f"{Fore.RED}[!] Could not detect local subnet!{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}[i] Detected Subnet: {Fore.CYAN}{subnet}.x{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Scanning for RTSP cameras (port 554)...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] This may take a few minutes...{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}{'─'*50}{Style.RESET_ALL}\n")
    
    ips = [f"{subnet}.{i}" for i in range(1, 255)]
    results = []
    results_lock = threading.Lock()
    
    # Worker function
    def worker(ip_list):
        for ip in ip_list:
            scan_rtsp_ip(ip, results, results_lock)
    
    # Create threads
    THREADS = 80
    chunks = [ips[i::THREADS] for i in range(THREADS)]
    threads = []
    
    start_time = time.time()
    
    for chunk in chunks:
        t = threading.Thread(target=worker, args=(chunk,), daemon=True)
        t.start()
        threads.append(t)
    
    # Wait for all threads
    for t in threads:
        t.join()
    
    elapsed = time.time() - start_time
    
    # Display results
    print(f"\n{Fore.CYAN}{'═'*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[✓] SCAN COMPLETE!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═'*50}{Style.RESET_ALL}\n")
    
    if results:
        print(f"{Fore.RED}[*] Found {len(results)} RTSP CAMERAS:{Style.RESET_ALL}\n")
        for idx, r in enumerate(results, 1):
            print(f"{Fore.CYAN}[{idx}] {r['ip']}{Style.RESET_ALL}")
            print(f"    Name: {Fore.YELLOW}{r['name']}{Style.RESET_ALL}")
            print(f"    RTSP URL: {Fore.WHITE}{r['rtsp_url']}{Style.RESET_ALL}")
            print()
        
        # Save to file
        try:
            with open("NeighboursCameras_Results.txt", 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("NEIGHBOURS CAMERA SCAN - RTSP CAMERAS FOUND\n")
                f.write("="*60 + "\n\n")
                for r in results:
                    f.write(f"IP: {r['ip']}\n")
                    f.write(f"Name: {r['name']}\n")
                    f.write(f"RTSP URL: {r['rtsp_url']}\n")
                    f.write("-"*60 + "\n\n")
            print(f"{Fore.GREEN}[✓] Results saved to: NeighboursCameras_Results.txt{Style.RESET_ALL}")
        except:
            pass
    else:
        print(f"{Fore.YELLOW}[!] No RTSP cameras found on local network{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}[i] Total IPs scanned: 254{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Cameras found: {len(results)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Time taken: {elapsed:.2f} seconds{Style.RESET_ALL}")


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_menu():
    """Print main menu"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Select Mode:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1.{Style.RESET_ALL} 🔍 Trace Route")
    print(f"{Fore.RED}2.{Style.RESET_ALL} ⚡ SUPER FAST SCAN (Camera Scanner)")
    print(f"{Fore.GREEN}3.{Style.RESET_ALL} 📷 Neighbours Camera Scanner")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Exit")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")


def main():
    """Main function"""
    while True:
        try:
            # Clear screen at start
            clear_screen()
            
            print_banner()
            
            # Display system info
            try:
                timestamp = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
                print(f"{Fore.GREEN}[i]{Style.RESET_ALL} Time: {Fore.YELLOW}{timestamp}{Style.RESET_ALL}")
            except:
                pass
            
            # Display network info
            try:
                gateway = get_default_gateway()
                local_ip = get_local_ip()
                print(f"{Fore.GREEN}[i]{Style.RESET_ALL} Your Local IP: {Fore.CYAN}{local_ip}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[i]{Style.RESET_ALL} Router Gateway: {Fore.CYAN}{gateway}{Style.RESET_ALL}")
            except:
                pass
            
            # Show menu
            print_menu()
            choice = input(f"{Fore.GREEN}Enter your choice (1-4): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                # Trace Route
                trace_route()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '2':
                # Super Fast Scan
                super_fast_scan()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '3':
                # Neighbours Camera Scanner
                neighbours_camera_scanner()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '4':
                # Exit
                print(f"\n{Fore.GREEN}[✓] Goodbye!{Style.RESET_ALL}\n")
                break
                
            else:
                print(f"{Fore.RED}[!] Invalid choice. Please select 1-4.{Style.RESET_ALL}")
                time.sleep(1)
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}[!] Interrupted by user{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
            time.sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)

