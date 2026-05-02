import socket
from subprocess import Popen
import time
import xml.etree.ElementTree as ET
import re
from pathlib import Path

def is_port_open(port):
    """Verifica se a porta TCP especificada está aberta."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def extrair_portas_appsettings(config_file: Path) -> list[int]:
    """
    Extrai as portas do arquivo appsettings.xml (C#).
    """
    if not config_file.exists():
        print(f"⚠️  Arquivo de configuração não encontrado: {config_file}")
        return []
    
    try:
        tree = ET.parse(config_file)
        root = tree.getroot()
        portas = []
        config = {}
    
    # Procura por todos os elementos 'add' dentro de 'appSettings'
        for item in root.findall('.//appSettings/add'):
            key = item.get('key')
            value = item.get('value')
            config[key] = value
        if "Port" in config.keys():
            portas.append(int(config["Port"]))
        if "HttpPort" in config.keys():
            portas.append(int(config["HttpPort"]))
        if "ApiPort" in config.keys():
            portas.append(int(config["ApiPort"]))
        return sorted(portas)
    except ET.ParseError as e:
        print(f"❌ Erro ao ler XML: {e}")
        return []
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")
        return []

def aguardar_wcf_iniciar(processorAtributes: Popen[bytes], config_file: Path = None, port: int = None):
    """
    Aguarda o WCF (Host) abrir a porta configurada.
    
    Prioridade:
    1. Se 'port' for fornecido, usa essa porta
    2. Se 'config_file' for fornecido, extrai as portas do appsettings.json
    3. Caso contrário, usa a porta padrão 8001
    """
    portas_verificar = []
    
    if port:
        portas_verificar = [port]
    elif config_file:
        portas_verificar = extrair_portas_appsettings(config_file)
    
    print(f"⏳ Aguardando WCF (PID: {processorAtributes.pid}) abrir porta(s) {portas_verificar}...")
    
    while processorAtributes.poll() is None: 
        if all(is_port_open(p) for p in portas_verificar):
            print("✅ Sinal verde! O Host está totalmente pronto.")
            break 
        # Pausa de meio segundo para não fritar a CPU do usuário num loop infinito
        time.sleep(0.5)