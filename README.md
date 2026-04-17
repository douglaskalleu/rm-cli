# 🖥️ RM CLI - Gerenciador de Aplicações RM

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

### Opção 1: Usar o .bat (mais simples)

1. Adicione a pasta `C:\rmc` ao seu **PATH** do Windows:
   - Pesquise "Variáveis de Ambiente" no menu Iniciar
   - Em "Path" do usuário, adicione: `C:\rmc`

2. Configure o caminho base:
   ```cmd
   rmc config --base-path "C:\SuaPasta"
   ```

3. Pronto! Use os comandos abaixo.

### Opção 2: Instalar como pacote Python

```cmd
cd C:\Users\Public\rmc
pip install -e .
```

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

A configuração fica salva em: `%USERPROFILE%\.rmc\config.json`

## 📋 Todos os Comandos

| Comando | Descrição |
|---------|-----------|
| `rmc config --base-path "..."` | Define o caminho base |
| `rmc config` | Mostra configuração atual |
| `rmc list` | Lista todas as versões |
| `rmc start host` | Inicia rm.host.exe (Atual) |
| `rmc start rm` | Inicia rm.exe (Atual) |
| `rmc start host  VERSAO` | Inicia rm.host.exe (Legado) |
| `rmc start rm  VERSAO` | Inicia rm.exe (Legado) |
| `rmc start-all` | Inicia host + rm (Atual) |
| `rmc start-all  VERSAO` | Inicia host + rm (Legado) |
| `rmc where host/rm [ VERSAO]` | Mostra caminho do executável |
