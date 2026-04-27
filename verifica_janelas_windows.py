import ctypes
from subprocess import Popen
import time

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

def obter_titulo_janela_por_pid(target_pid):
    """Retorna o título da janela visível que pertence ao PID informado."""
    titulos = []
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            pid_janela = ctypes.c_ulong()
            GetWindowThreadProcessId(hwnd, ctypes.byref(pid_janela))
            
            if pid_janela.value == target_pid:
                length = GetWindowTextLength(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buff, length + 1)
                    titulos.append(buff.value)
        return True
    
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titulos[0] if titulos else None

def aguardar_wcf_iniciar(processorAtributes:Popen[bytes]):
    print(f"⏳ Aguardando WCF (PID: {processorAtributes.pid}) mudar o status para 'Iniciado'...")
    
    status_atual = ""
    
    while processorAtributes.poll() is None: 
        titulo = obter_titulo_janela_por_pid(processorAtributes.pid)
        
        if titulo and titulo != status_atual:
            status_atual = titulo
            # Condição de parada: achou a palavra "Iniciado"
            if "INICIADO" in titulo:
                print("✅ Sinal verde! O Host está totalmente pronto.")
                break 
                
        # Pausa de meio segundo para não fritar a CPU do usuário num loop infinito
        time.sleep(0.5)