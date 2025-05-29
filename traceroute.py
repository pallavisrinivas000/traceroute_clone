import socket
import time

target_host = "google.com"
port = 33434
timeout = 5.0
max_hops = 10

print(f"Traceroute to {target_host}")

for ttl in range(1, max_hops + 1):
    print(f"\n[DEBUG] TTL = {ttl}")

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    recv_socket.settimeout(timeout)
    recv_socket.bind(("", port))

    start_time = time.time()
    send_socket.sendto(b'', (target_host, port))

    curr_addr = None
    try:
        data, addr = recv_socket.recvfrom(1024)
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        curr_addr = addr[0]
    except socket.timeout:
        curr_addr = "Request timed out"
    finally:
        send_socket.close()
        recv_socket.close()
    
    if curr_addr == socket.gethostbyname(target_host):
        print("Destination reached")
        break