# 🖥️ RM CLI - Gerenciador ### 🚀 Instalação automática (recomendado)

1. **Baixe o instalador:** [📥 Clique aqui para baixar](https://github.com/douglaskalleu/rm-cli/releases/latest/download/install.bat)
2. **Execute** o `install.bat` (clique duplo)plicações RM

CLI em Python para iniciar `rm.host.exe`, `rm.exe` e `rm.atualizador.exe`  direto do terminal, sem navegar pelas pastas.

## 📁 Estrutura esperada

```
C:\SuaPasta\
├── Atual\
│   └──Release\
│      └── bin\
│          ├── rm.host.exe
│          └── rm.exe
└── Legado\
    ├── 12.1.2510\
    │   └── bin\
    │       ├── rm.host.exe
    │       └── rm.exe
    ├── 12.1.2602\
    │   └── bin\
    │       ├── rm.host.exe
    │       └── rm.exe
    └── ...
```

## ⚡ Instalação Rápida

### 🚀 Instalação automática (recomendado)

1. **Baixe o instalador:** [📥 install.bat | Versão: 1.0.0](https://raw.githubusercontent.com/douglaskalleu/rm-cli/master/install.bat)
2. **Execute** o `install.bat` (clique duplo)
3. **Feche e reabra** o terminal
4. **Configure** o caminho base:
   ```cmd
   rmc config --base-path "C:\SuaPasta"
   ```
5. Pronto! 🎉

> O instalador baixa os arquivos, cria a pasta `%USERPROFILE%\rmc-cli` e adiciona ao PATH automaticamente.

---

### Instalação manual

<details>
<summary>Opção 1: Usar o .bat</summary>

1. Baixe os arquivos `rm_cli.py` e `rmc.bat` do repositório
2. Coloque numa pasta (ex: `C:\rmc-cli`)
3. Adicione essa pasta ao **PATH** do Windows:
   - Pesquise "Variáveis de Ambiente" no menu Iniciar
   - Em "Path" do usuário, adicione o caminho da pasta
4. Configure:
   ```cmd
   rmc config --base-path "C:\SuaPasta"
   ```

</details>

<details>
<summary>Opção 2: Instalar como pacote Python</summary>

```cmd
git clone https://github.com/douglaskalleu/rm-cli.git
cd rm-cli
pip install -e .
```

</details>

## 🚀 Como Usar

### Configurar (primeira vez)

```cmd
rmc config --base-path "C:\SuaPasta"
```

### Ver configuração atual

```cmd
rmc config
```

### Listar versões disponíveis

```cmd
rmc list
```

### Iniciar aplicações da versão ATUAL

```cmd
rmc start host          # Inicia rm.host.exe
rmc start rm            # Inicia rm.exe
rmc start-all           # Inicia host + rm juntos
```

### Iniciar aplicações do LEGADO

```cmd
rmc start host 12.1.2510      # Inicia rm.host.exe da versão 12.1.2510
rmc start rm 12.1.2602        # Inicia rm.exe da versão 12.1.2602
rmc start-all 12.1.2510       # Inicia host + rm da versão 12.1.2510
```

### Busca parcial de versão

Se você não lembrar a versão completa:

```cmd
rmc start host 2510           # Encontra 12.1.2510 automaticamente
```

### Ver caminho do executável

```cmd
rmc where host                    # Mostra caminho do rm.host.exe (Atual)
rmc where rm 12.1.2510        # Mostra caminho do rm.exe (Legado)
```

## ⚙️ Configurações Avançadas

Se sua estrutura de pastas tiver nomes diferentes:

```cmd
rmc config --atual-folder "Release"
rmc config --legado-folder "Versoes"
rmc config --bin-folder "binaries"
```

A configuração fica salva em: `%USERPROFILE%\.rm\config.json`

## 📋 Todos os Comandos

| Comando | Descrição |
|---------|-----------|
| `rmc config --base-path "..."` | Define o caminho base |
| `rmc config` | Mostra configuração atual |
| `rmc list` | Lista todas as versões |
| `rmc start host` | Inicia rm.host.exe (Atual) |
| `rmc start rm` | Inicia rm.exe (Atual) |
| `rmc start host VERSAO` | Inicia rm.host.exe (Legado) |
| `rmc start rm VERSAO` | Inicia rm.exe (Legado) |
| `rmc start-all` | Inicia host + rm (Atual) |
| `rmc start-all VERSAO` | Inicia host + rm (Legado) |
| `rmc kill` | Encerra todos os processos RM |
| `rmc kill host` | Encerra apenas rm.host.exe |
| `rmc kill rm` | Encerra apenas rm.exe |
| `rmc where host` | Mostra caminho do executável (Atual) |
| `rmc where rm VERSAO` | Mostra caminho do executável (Legado) |
