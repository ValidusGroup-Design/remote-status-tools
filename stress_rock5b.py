import time
import multiprocessing
import os
import socket
import psutil

def stress_cpu():
    """Generate CPU load."""
    while True:
        pass

def get_cpu_temps():
    """Return thermal zone temps as a dictionary."""
    temps = {}
    for zone in os.listdir('/sys/class/thermal'):
        if zone.startswith("thermal_zone"):
            try:
                with open(f'/sys/class/thermal/{zone}/type') as f:
                    zone_type = f.read().strip()
                with open(f'/sys/class/thermal/{zone}/temp') as f:
                    temp_millic = int(f.read().strip())
                temps[zone_type] = temp_millic / 1000.0
            except Exception:
                continue
    return temps

def get_network_info():
    """Return hostname, IP, and MAC addresses."""
    hostname = socket.gethostname()
    interfaces = psutil.net_if_addrs()

    net_info = []
    for iface, addrs in interfaces.items():
        mac = ip = None
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip = addr.address
            elif addr.family == psutil.AF_LINK:
                mac = addr.address
        if ip and mac:
            net_info.append((iface, ip, mac))

    return hostname, net_info

if __name__ == "__main__":
    print("[*] Gathering system info...")
    hostname, net_if_data = get_network_info()
    print(f"Hostname: {hostname}")
    for iface, ip, mac in net_if_data:
        print(f"Interface: {iface:<10} IP: {ip:<15} MAC: {mac}")

    print("\n[*] Spawning 8 CPU stress processes...")
    workers = []
    for _ in range(8):
        p = multiprocessing.Process(target=stress_cpu)
        p.start()
        workers.append(p)

    print("[*] Running stress for 15 seconds...")
    time.sleep(15)

    print("[*] Terminating processes...")
    for p in workers:
        p.terminate()
        p.join()

    print("\n[*] CPU Temperature Sensors:")
    temps = get_cpu_temps()
    for label, temp in temps.items():
        print(f" - {label:20}: {temp:.1f} °C")
