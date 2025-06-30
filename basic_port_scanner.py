#!/usr/bin/env python3
"""
Escáner de puertos básico - Versión educativa
Este script demuestra los principios básicos detrás de herramientas como Nmap
"""

import socket
import sys
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
import argparse

class SimplePortScanner:
    def __init__(self, target_host, timeout=1):
        """
        Inicializa el escáner con el host objetivo y timeout
        
        Args:
            target_host (str): Dirección IP o nombre del host a escanear
            timeout (int): Tiempo límite para cada conexión en segundos
        """
        self.target_host = target_host
        self.timeout = timeout
        self.open_ports = []
        
        # Intentar resolver el nombre del host a IP
        try:
            self.target_ip = socket.gethostbyname(target_host)
        except socket.gaierror:
            print(f"Error: No se pudo resolver el host {target_host}")
            sys.exit(1)
    
    def scan_port(self, port):
        """
        Escanea un puerto específico usando conexión TCP
        
        Args:
            port (int): Número de puerto a escanear
            
        Returns:
            dict: Información sobre el puerto escaneado
        """
        try:
            # Crear un socket TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Configurar timeout para evitar que el programa se cuelgue
                sock.settimeout(self.timeout)
                
                # Intentar conectar al puerto
                result = sock.connect_ex((self.target_ip, port))
                
                if result == 0:
                    # El puerto está abierto
                    service = self.get_service_name(port)
                    return {
                        'port': port,
                        'status': 'abierto',
                        'service': service
                    }
                else:
                    # El puerto está cerrado o filtrado
                    return {
                        'port': port,
                        'status': 'cerrado',
                        'service': None
                    }
                    
        except socket.timeout:
            # Timeout - probablemente filtrado
            return {
                'port': port,
                'status': 'filtrado',
                'service': None
            }
        except Exception as e:
            # Otro error
            return {
                'port': port,
                'status': 'error',
                'service': None,
                'error': str(e)
            }
    
    def get_service_name(self, port):
        """
        Intenta obtener el nombre del servicio común para un puerto
        
        Args:
            port (int): Número de puerto
            
        Returns:
            str: Nombre del servicio o 'desconocido'
        """
        common_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S'
        }
        
        return common_ports.get(port, 'desconocido')
    
    def scan_range(self, start_port, end_port, max_threads=50):
        """
        Escanea un rango de puertos usando múltiples hilos para mayor velocidad
        
        Args:
            start_port (int): Puerto inicial del rango
            end_port (int): Puerto final del rango
            max_threads (int): Número máximo de hilos concurrentes
        """
        print(f"Iniciando escaneo de {self.target_host} ({self.target_ip})")
        print(f"Escaneando puertos {start_port}-{end_port}")
        print(f"Tiempo de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # Usar ThreadPoolExecutor para escaneo paralelo
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            # Crear lista de puertos a escanear
            ports_to_scan = range(start_port, end_port + 1)
            
            # Ejecutar escaneo en paralelo
            results = list(executor.map(self.scan_port, ports_to_scan))
        
        # Procesar y mostrar resultados
        open_ports = [r for r in results if r['status'] == 'abierto']
        
        if open_ports:
            print(f"\nPuertos abiertos encontrados en {self.target_host}:")
            print(f"{'Puerto':<8} {'Servicio':<12} {'Estado'}")
            print("-" * 30)
            
            for port_info in open_ports:
                print(f"{port_info['port']:<8} {port_info['service']:<12} {port_info['status']}")
                self.open_ports.append(port_info['port'])
        else:
            print(f"\nNo se encontraron puertos abiertos en el rango especificado.")
        
        print(f"\nEscaneo completado en: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total de puertos abiertos: {len(open_ports)}")
    
    def ping_host(self):
        """
        Verifica si el host está disponible intentando conectar al puerto 80
        Esta es una versión simplificada de ping usando TCP
        
        Returns:
            bool: True si el host responde, False en caso contrario
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                # Intentar conectar a un puerto común
                result = sock.connect_ex((self.target_ip, 80))
                return True  # Si llegamos aquí, el host responde
        except:
            try:
                # Intentar con otro puerto común
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(2)
                    result = sock.connect_ex((self.target_ip, 443))
                    return True
            except:
                return False

def main():
    """
    Función principal que maneja argumentos de línea de comandos
    """
    parser = argparse.ArgumentParser(
        description='Escáner de puertos simple - Versión educativa',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python scanner.py google.com
  python scanner.py 192.168.1.1 -p 1-1000
  python scanner.py localhost -p 80,443,8080
        """
    )
    
    parser.add_argument('host', help='Host o IP a escanear')
    parser.add_argument('-p', '--ports', default='1-100',
                       help='Puertos a escanear (ej: 1-100, 80,443,8080)')
    parser.add_argument('-t', '--timeout', type=int, default=1,
                       help='Timeout en segundos (default: 1)')
    parser.add_argument('--threads', type=int, default=50,
                       help='Número de hilos (default: 50)')
    
    args = parser.parse_args()
    
    # Crear instancia del escáner
    scanner = SimplePortScanner(args.host, args.timeout)
    
    # Verificar si el host está disponible
    print("Verificando disponibilidad del host...")
    if not scanner.ping_host():
        print(f"Advertencia: El host {args.host} podría no estar disponible")
        response = input("¿Continuar con el escaneo? (s/n): ")
        if response.lower() != 's':
            print("Escaneo cancelado.")
            return
    
    # Parsear puertos
    try:
        if '-' in args.ports:
            # Rango de puertos
            start, end = map(int, args.ports.split('-'))
            scanner.scan_range(start, end, args.threads)
        elif ',' in args.ports:
            # Lista de puertos específicos
            ports = [int(p.strip()) for p in args.ports.split(',')]
            print(f"Escaneando puertos específicos: {ports}")
            
            with ThreadPoolExecutor(max_workers=args.threads) as executor:
                results = list(executor.map(scanner.scan_port, ports))
            
            open_ports = [r for r in results if r['status'] == 'abierto']
            if open_ports:
                print(f"\nPuertos abiertos encontrados:")
                for port_info in open_ports:
                    print(f"Puerto {port_info['port']}: {port_info['service']} ({port_info['status']})")
            else:
                print("\nNo se encontraron puertos abiertos.")
        else:
            # Puerto único
            port = int(args.ports)
            result = scanner.scan_port(port)
            print(f"Puerto {port}: {result['status']}")
            if result['service']:
                print(f"Servicio: {result['service']}")
                
    except ValueError:
        print("Error: Formato de puertos inválido")
        print("Usa: 1-100 (rango), 80,443,8080 (lista), o 80 (puerto único)")

if __name__ == "__main__":
    main()