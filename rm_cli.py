import os
import sys
import json
import subprocess
import argparse
import urllib.request
from pathlib import Path
from verifica_janelas_windows import aguardar_wcf_iniciar
VERSION = "1.2.1"

GITHUB_RAW = "https://raw.githubusercontent.com/douglaskalleu/rm-cli/master"
PID_HOST = 0
# Configuração
CONFIG_DIR = Path.home() / ".rm"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_CONFIG = {
    "base_path": "",
    "atual_folder": "Atual",
    "release_folder": "Release",
    "legado_folder": "Legado",
    "bin_folder": "bin",
    "host_exe": "rm.host.exe",
    "rm_exe": "rm.exe",
    "atualizador_exe": "rm.atualizador.exe",
}

# Funções de Configuração
def load_config() -> dict:
    """Carrega a configuração do arquivo JSON, mesclando com defaults."""
    config = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config.update(json.load(f))
    return config


def save_config(config: dict):
    """Salva a configuração no arquivo JSON."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_base_path(config: dict) -> Path:
    """Retorna o caminho base configurado."""
    bp = config.get("base_path", "")
    if not bp:
        print("❌ Caminho base não configurado!")
        print("   Execute: rm config --base-path \"C:\\caminho\\para\\sua\\estrutura\"")
        sys.exit(1)
    return Path(bp)

# Resolução de Caminhos
def get_atual_bin(config: dict) -> Path:
    """Retorna o caminho da pasta bin da versão Atual."""
    base = get_base_path(config)
    release_path = base / config["atual_folder"] / config["release_folder"]
    return release_path / config["bin_folder"]


def get_legado_versions(config: dict) -> list[str]:
    """Lista todas as versões disponíveis na pasta Legado."""
    base = get_base_path(config)
    legado_path = base / config["legado_folder"]
    if not legado_path.exists():
        return []
    versions = []
    for item in sorted(legado_path.iterdir()):
        if item.is_dir():
            bin_path = item / config["bin_folder"]
            if bin_path.exists():
                versions.append(item.name)
    return versions


def get_legado_bin(config: dict, version: str) -> Path:
    """Retorna o caminho da pasta bin de uma versão Legado específica."""
    base = get_base_path(config)
    return base / config["legado_folder"] / version / config["bin_folder"]

# Execução 
def start_process(exe_path: Path):
    """Inicia um executável em processo separado."""
    if not exe_path.exists():
        print(f"❌ Arquivo não encontrado: {exe_path}")
        sys.exit(1)

    print(f"🚀 Iniciando: {exe_path}")
    try:
        os.chdir(exe_path.parent)
        proc= subprocess.Popen(str(exe_path),creationflags=subprocess.CREATE_NEW_CONSOLE)
        print(f"✅ {exe_path.name} iniciado com sucesso!")
        return proc
    except Exception as e:
        print(f"❌ Erro ao iniciar {exe_path.name}: {e}")
        sys.exit(1)

# Comandos do CLI
def cmd_version(args, config: dict):
    """Comando: version - Mostra a versão atual."""
    print(f"🖥️  RMC CLI v{VERSION}")


def cmd_update(args, config: dict):
    """Comando: update - Atualiza o CLI para a última versão."""
    print(f"🔄 Versão atual: v{VERSION}")
    print("📡 Verificando atualizações no GitHub...")

    # Descobrir onde o CLI está instalado (pasta do próprio script)
    install_dir = Path(__file__).resolve().parent

    try:
        # Baixar versão remota para checar
        remote_url = f"{GITHUB_RAW}/rm_cli.py"
        req = urllib.request.Request(remote_url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            remote_content = resp.read().decode("utf-8")

        # Extrair versão remota
        remote_version = None
        for line in remote_content.splitlines():
            if line.startswith("VERSION"):
                remote_version = line.split('"')[1]
                break

        if not remote_version:
            print("❌ Não foi possível verificar a versão remota.")
            return

        if remote_version == VERSION:
            print(f"✅ Você já está na versão mais recente (v{VERSION}).")
            return

        print(f"🆕 Nova versão disponível: v{remote_version}")
        print(f"📂 Atualizando em: {install_dir}")
        print()

        # Baixar e sobrescrever rm_cli.py
        cli_path = install_dir / "rm_cli.py"
        with open(cli_path, "w", encoding="utf-8") as f:
            f.write(remote_content)
        print("✅ rm_cli.py atualizado!")

        # Baixar e sobrescrever rmc.bat
        bat_url = f"{GITHUB_RAW}/rmc.bat"
        bat_path = install_dir / "rmc.bat"
        urllib.request.urlretrieve(bat_url, str(bat_path))
        print("✅ rmc.bat atualizado!")

        print(f"\n🎉 Atualizado para v{remote_version}!")

    except Exception as e:
        print(f"❌ Erro ao atualizar: {e}")


def cmd_kill(args, config: dict):
    """Comando: kill - Encerra processos RM conhecidos."""
    app = getattr(args, "app", None)

    if app:
        # Matar processo específico
        app = app.lower()
        if app in ("host", "rm.host", "rm.host.exe"):
            targets = [config.get("host_exe", "rm.host.exe")]
        elif app in ("rm", "rm.exe"):
            targets = [config.get("rm_exe", "rm.exe")]
        elif app in ("atualizador", "rm.atualizador", "rm.atualizador.exe"):
            targets = [config.get("atualizador_exe", "rm.atualizador.exe")]
        else:
            print(f"❌ Aplicação desconhecida: '{app}'")
            sys.exit(1)
        print(f"⚠️  Encerrando {targets[0]}...")
    else:
        # Matar todos os processos RM
        targets = [
            config.get("host_exe", "rm.host.exe"),
            config.get("rm_exe", "rm.exe"),
            config.get("atualizador_exe", "rm.atualizador.exe"),
        ]
        print("⚠️  Encerrando todos os processos RM...")

    killed = 0
    for proc in targets:
        result = subprocess.run(
            ["taskkill", "/F", "/IM", proc],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"✅ {proc} encerrado!")
            killed += 1

    if killed == 0:
        print("ℹ️  Nenhum processo RM encontrado rodando.")
    else:
        print(f"\n🏁 {killed} processo(s) encerrado(s).")


def cmd_start(args, config: dict):
    """Comando: start - Inicia rm.exe ou rm.host.exe."""
    app = args.app.lower()

    # Determinar qual executável
    if app in ("host", "rm.host", "rm.host.exe"):
        exe_name = config["host_exe"]
    elif app in ("rm", "rm.exe"):
        exe_name = config["rm_exe"]
    elif app in ("atualizador", "rm.atualizador", "rm.atualizador.exe"):
        exe_name = config["atualizador_exe"]
    else:
        print(f"❌ Aplicação desconhecida: '{app}'")
        print("   Use: host | rm | atualizador")
        sys.exit(1)

    version = args.version

    if version is None or version.lower() == "atual":
        bin_path = get_atual_bin(config)
        label = "Atual/Release"
    else:
        available = get_legado_versions(config)
        # match exato
        if version in available:
            bin_path = get_legado_bin(config, version)
            label = f"Legado/{version}"
        else:
            # match parcial
            matches = [v for v in available if version in v]
            if len(matches) == 1:
                bin_path = get_legado_bin(config, matches[0])
                label = f"Legado/{matches[0]}"
            elif len(matches) > 1:
                print(f"⚠️  Múltiplas versões encontradas para '{version}':")
                for m in matches:
                    print(f"   • {m}")
                print("   Seja mais específico.")
                sys.exit(1)
            else:
                print(f"❌ Versão '{version}' não encontrada no Legado.")
                print(f"   Versões disponíveis: {', '.join(available) if available else 'nenhuma'}")
                sys.exit(1)

    exe_path = bin_path / exe_name
    print(f"📂 Versão: {label}")
    start_process(exe_path)


def cmd_start_all(args, config: dict):
    """Comando: start-all - Inicia host e rm juntos."""
    version = args.version
    
    if version is None or version.lower() == "atual":
        bin_path = get_atual_bin(config)
        label = "Atual/Release"
    else:
        available = get_legado_versions(config)
        if version in available:
            bin_path = get_legado_bin(config, version)
            label = f"Legado/{version}"
        else:
            matches = [v for v in available if version in v]
            if len(matches) == 1:
                bin_path = get_legado_bin(config, matches[0])
                label = f"Legado/{matches[0]}"
            elif len(matches) > 1:
                print(f"⚠️  Múltiplas versões encontradas para '{version}':")
                for m in matches:
                    print(f"   • {m}")
                sys.exit(1)
            else:
                print(f"❌ Versão '{version}' não encontrada.")
                sys.exit(1)

    print(f"📂 Versão: {label}")
    print()

    host_path = bin_path / config["host_exe"]
    rm_path = bin_path / config["rm_exe"]
    procServer=start_process(host_path)
    aguardar_wcf_iniciar(procServer)
    print()
    start_process(rm_path)


def cmd_list(args, config: dict):
    """Comando: list - Lista versões disponíveis."""

    atual_bin = get_atual_bin(config)
    has_host = (atual_bin / config["host_exe"]).exists()
    has_rm = (atual_bin / config["rm_exe"]).exists()

    print("╔══════════════════════════════════════════════════════╗")
    print("║              📋 Versões Disponíveis                  ║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║                                                      ║")

    if atual_bin.exists():
        print(f"║  🟢 Atual (release)                                  ║")
    else:
        print(f"║  🔴 Atual - pasta não encontrada                     ║")

    print("║                                                      ║")
    print("║  📦 Legado:                                          ║")

    versions = get_legado_versions(config)
    if versions:
        for v in versions:
            v_bin = get_legado_bin(config, v)
            v_host = "✅" if (v_bin / config["host_exe"]).exists() else "❌"
            v_rm = "✅" if (v_bin / config["rm_exe"]).exists() else "❌"
            print(f"║     🔵 {v}                                     ║")
    else:
        print("║     (nenhuma versão encontrada)")

    print("║                                                      ║")
    print("╚══════════════════════════════════════════════════════╝")


def cmd_config(args, config: dict):
    """Comando: config - Configura o CLI."""
    changed = False

    if args.base_path:
        path = os.path.abspath(args.base_path)
        config["base_path"] = path
        changed = True
        print(f"✅ Caminho base definido: {path}")

    if args.atual_folder:
        config["atual_folder"] = args.atual_folder
        changed = True
        print(f"✅ Pasta Atual definida: {args.atual_folder}")

    if args.release_folder:
        config["release_folder"] = args.release_folder
        changed = True
        print(f"✅ Pasta Release definida: {args.release_folder}")

    if args.legado_folder:
        config["legado_folder"] = args.legado_folder
        changed = True
        print(f"✅ Pasta Legado definida: {args.legado_folder}")

    if args.bin_folder:
        config["bin_folder"] = args.bin_folder
        changed = True
        print(f"✅ Pasta bin definida: {args.bin_folder}")

    if changed:
        save_config(config)
        print(f"\n💾 Configuração salva em: {CONFIG_FILE}")
    else:
        print("╔══════════════════════════════════════════════════════╗")
        print("║              ⚙️  Configuração Atual                  ║")
        print("╠══════════════════════════════════════════════════════╣")
        for key, value in config.items():
            print(f"  {key:20s} = {value}")
        print("╚══════════════════════════════════════════════════════╝")
        print(f"\n📁 Arquivo: {CONFIG_FILE}")


def cmd_where(args, config: dict):
    """Comando: where - Mostra o caminho de um executável."""
    app = args.app.lower()
    version = args.version

    if app in ("host", "rm.host", "rm.host.exe"):
        exe_name = config["host_exe"]
    elif app in ("rm", "rm.exe"):
        exe_name = config["rm_exe"]
    else:
        print(f"❌ Aplicação desconhecida: '{app}'")
        sys.exit(1)

    if version is None or version.lower() == "atual":
        bin_path = get_atual_bin(config)
    else:
        bin_path = get_legado_bin(config, version)

    exe_path = bin_path / exe_name
    exists = "✅" if exe_path.exists() else "❌"
    print(f"{exists} {exe_path}")

# CLI Principal
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rm",
        description="🖥️  RM CLI - Gerenciador de aplicações RM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  param: APLICATIVO = host | rm | atualizador
  param: VERSÃO DESEJADA = parte ou nome completo da pasta de versão no Legado (ex: 12.1.2510)

  rmc config --base-path "C:\\RM\\Projetos"
  rmc list                                           # Lista versões disponíveis

  ==== START ====
  rmc start [APLICATIVO]                             # Inicia aplicativo da versão Atual
  rmc start-all                                      # Inicia host + rm da versão Atual
  rmc start [APLICATIVO] [VERSÃO DESEJADA]           # Inicia aplicativo do Legado
  rmc start-all [VERSÃO DESEJADA]                    # Inicia host + rm do Legado

  ==== WHERE ====
  rmc where [APLICATIVO] [VERSÃO DESEJADA]           # Mostra caminho do executável (ex: rm where rm 2510)

  ==== KILL ====
  rmc kill host                                      # Encerra apenas rm.host.exe
  rmc kill rm                                        # Encerra apenas rm.exe
  rmc kill                                           # Encerra todos os processos RM
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")

    # start
    p_start = subparsers.add_parser("start", help="Inicia rm.exe ou rm.host.exe")
    p_start.add_argument(
        "app",
        choices=["host", "rm", "rm.host", "rm.host.exe", "rm.exe", "atualizador", "rm.atualizador", "rm.atualizador.exe"],
        help="Aplicação para iniciar (host | rm | atualizador)",
    )
    p_start.add_argument(
        "version",
        nargs="?",
        default=None,
        help="Versão do Legado (ex: 12.1.2510). Padrão: Atual",
    )

    # start-all
    p_start_all = subparsers.add_parser("start-all", help="Inicia host + rm juntos")
    p_start_all.add_argument(
        "version",
        nargs="?",
        default=None,
        help="Versão do Legado. Padrão: Atual",
    )

    # list
    subparsers.add_parser("list", help="Lista versões disponíveis")

    # update
    subparsers.add_parser("update", help="Atualiza o CLI para a última versão")

    # version
    subparsers.add_parser("version", help="Mostra a versão atual")

    # kill
    p_kill = subparsers.add_parser("kill", help="Encerra processos RM (todos ou específico)")
    p_kill.add_argument(
        "app",
        nargs="?",
        default=None,
        choices=["host", "rm", "rm.host", "rm.host.exe", "rm.exe", "atualizador", "rm.atualizador", "rm.atualizador.exe"],
        help="Aplicação para encerrar (host | rm | atualizador). Se omitido, encerra todos.",
    )

    # config
    p_config = subparsers.add_parser("config", help="Configura o CLI")
    p_config.add_argument("--base-path", help="Caminho base da estrutura RM")
    p_config.add_argument("--atual-folder", help="Nome da pasta Atual (padrão: Atual)")
    p_config.add_argument("--release-folder", help="Nome da pasta Release dentro de Atual (padrão: Release)")  
    p_config.add_argument("--legado-folder", help="Nome da pasta Legado (padrão: Legado)")
    p_config.add_argument("--bin-folder", help="Nome da pasta bin (padrão: bin)")

    # where
    p_where = subparsers.add_parser("where", help="Mostra o caminho de um executável")
    p_where.add_argument(
        "app",
        choices=["host", "rm", "rm.host", "rm.host.exe", "rm.exe"],
        help="Aplicação para localizar",
    )
    p_where.add_argument(
        "version",
        nargs="?",
        default=None,
        help="Versão do Legado. Padrão: Atual",
    )

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    config = load_config()

    commands = {
        "start": cmd_start,
        "start-all": cmd_start_all,
        "list": cmd_list,
        "config": cmd_config,
        "where": cmd_where,
        "kill": cmd_kill,
        "update": cmd_update,
        "version": cmd_version,
    }

    handler = commands.get(args.command)
    if handler:
        handler(args, config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
