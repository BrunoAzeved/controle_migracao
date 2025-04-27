# Controle de Migração

[![CI - Controle Migração](https://github.com/BrunoAzeved/controle_migracao/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/BrunoAzeved/controle_migracao/actions/workflows/ci.yml)

Este projeto é um sistema para gerenciar e monitorar o status de migração de fluxos e suas dependências. Ele foi desenvolvido utilizando **Streamlit** e **Pandas**.

## Funcionalidades

- **Dashboard Interativo**:
  - Exibe métricas como:
    - Total de fluxos migrados e não migrados.
    - Fluxos disponíveis para migração.
    - Fluxos não disponíveis para migração.
  - Identifica inconsistências, como fluxos marcados como migrados, mas indisponíveis para migração.

- **Atualização Automática**:
  - Atualiza o campo `Disponível para Migrar` no arquivo `controle_fluxos.csv` com base no status das dependências nos arquivos `data.csv` e `fluxos.csv`.

- **Gerenciamento de Fluxos**:
  - Permite marcar fluxos como migrados diretamente na interface.

## Estrutura do Projeto

```plaintext
controle_migracao/
├── archives/
│   ├── data.csv                # Status das tabelas
│   ├── fluxos.csv              # Dependências dos fluxos
│   ├── controle_fluxos.csv     # Status dos fluxos
├── pages/
│   ├── 01_Migração_Tabelas.py  # Página para controle das tabelas migradas
│   ├── 02_Fluxos.py            # Página para gerenciar fluxos
├── config.py                   # Configurações e funções auxiliares
├── Dashboard.py                # Arquivo principal do dashboard
├── .gitignore                  # Arquivo para ignorar arquivos no Git
└── README.md                   # Documentação do projeto
```

## Requisitos

- **Python**: Versão 3.8 ou superior.
- **Bibliotecas**:
  - `streamlit`
  - `pandas`

Instale as dependências com:

```bash
pip install -r requirements.txt
```

## Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/BrunoAzeved/controle_migracao.git
   cd controle_migracao
   ```

2. Inicie o dashboard:
   ```bash
   streamlit run Dashboard.py
   ```

Acesse o sistema no navegador para gerenciar os fluxos de migração.

## Contribuindo

Contribuições são bem-vindas! Abra issues ou envie pull requests para melhorias.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
