# 📋 Changelog

Todas as mudanças notáveis deste projeto serão documentadas aqui.

## [1.2.1] - 2026-04-27

### 🐛 Correções
- **start-all** - Corrigido ação do comando `rmc start-all` que retornada null ao tentar inciar o RM porque o HOST ainda não estava completamente iniciado

## [1.2.0] - 2026-04-17

### ✨ Novidades
- **update** - Comando `rmc update` atualiza o CLI direto do GitHub
- **version** - Comando `rmc version` mostra a versão instalada
- **install.bat** - Instalador automático (baixa Python se necessário, configura PATH)
- **release_folder** - Suporte à pasta Release dentro de Atual (`Atual/Release/bin`)

### 🐛 Correções
- **start** - Corrigido `rm.host.exe` que não abria na versão Atual (trocado `DETACHED_PROCESS` por `os.startfile`)
- **config** - Novas chaves do `DEFAULT_CONFIG` agora aparecem automaticamente sem precisar recriar o `config.json`

### 🔧 Melhorias
- Comando renomeado de `rm-cli` para `rmc`
- Versão do Legado agora é posicional (sem `-v`): `rmc start host 2510`
- **kill** aceita argumento opcional: `rmc kill host` ou `rmc kill` (todos)
- README atualizado com link de download direto do instalador

## [1.0.0] - 2026-04-16

### ✨ Primeiro Release

- **start** - Inicia `rm.host.exe`, `rm.exe` ou `rm.atualizador.exe` (Atual ou Legado)
- **start-all** - Inicia host + rm juntos
- **kill** - Encerra processos RM (todos ou específico)
- **list** - Lista versões disponíveis (Atual e Legado)
- **where** - Mostra o caminho de um executável
- **config** - Configura caminhos base, pastas e nomes dos executáveis
- Busca parcial de versão (ex: `rmc start host 2510` encontra `12.1.2510`)
- Configuração persistente em `~/.rm/config.json`
