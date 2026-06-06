# Laboratorio 3: Ataque DHCP Spoofing

## 🎥 Enlace del Video Demostrativo
[Haz clic aquí para ver la demostración del laboratorio en Google Drive]https://drive.google.com/file/d/191S5jj6CRNczlkFGdn8x1q4HAyI35-Q6/view?usp=drive_link

---

## 1. Objetivo del Laboratorio
El propósito de esta práctica es demostrar la vulnerabilidad del protocolo DHCP mediante el despliegue de un servidor DHCP no autorizado (Rogue DHCP Server). Se interceptan las solicitudes de los clientes de la red local para modificar sus parámetros IP de forma centralizada y desviar su tráfico a través de la máquina del atacante.

---

## 2. Objetivo del Script
El script desarrollado en Python y Scapy escucha las tramas de difusión DHCP en la red local. Al detectar un mensaje `DHCP DISCOVER`, responde con un `DHCP OFFER` asignando una dirección IP disponible. Posteriormente, al recibir el `DHCP REQUEST` del cliente, responde con un `DHCP ACK` consolidando el engaño e inyectando la IP del atacante como la Puerta de Enlace Predeterminada (Gateway).

---

## 3. Documentación de la Red
* **Mi Matrícula:** 2024-2421
* **Segmento de Red:** `10.24.21.0/24`
* **IP Atacante (Kali Linux):** `10.24.21.2`
* **IP Asignada de forma maliciosa:** `10.24.21.50`
* **Gateway Falso Configurado:** `10.24.21.2`

---

## 4. Evidencias / Capturas de Pantalla
<img width="1882" height="933" alt="image" src="https://github.com/user-attachments/assets/3ec255e8-9a06-443b-a7e0-ca5aaa5beaea" />
<img width="843" height="565" alt="image" src="https://github.com/user-attachments/assets/09b41230-4604-4e87-b1d8-80d904bdd2db" />


---

## 5. Medidas Técnicas de Mitigación (Hardening)
La contramedida estándar de la industria para prevenir la inclusión de servidores DHCP falsos es activar **DHCP Snooping** en los switches de acceso:

1. Se habilita la característica de forma global en la VLAN correspondiente.
2. Todos los puertos del switch pasan a ser "no confiables" (untrusted) por defecto, descartando cualquier paquete de respuesta DHCP (Offer/Ack) que intente ingresar por ellos.
3. Se configura explícitamente como "confiable" (trusted) únicamente el puerto del switch que conecta de forma directa con el router o el servidor DHCP centralizado legítimo.

### Ejemplo de comandos en Cisco:
```text
Switch(config)# ip dhcp snooping
Switch(config)# ip dhcp snooping vlan 1
Switch(config)# interface FastEthernet 0/1
Switch(config-if)# ip dhcp snooping trust
