# Controle de Migração

Este projeto é um sistema para gerenciar e monitorar o status de migração de fluxos e suas dependências. Ele foi desenvolvido utilizando **Streamlit** e **Pandas**.

## Funcionalidades Principais

- **Dashboard Interativo**:
  - Apresenta métricas como:
    - Total de fluxos migrados.
    - Total de fluxos não migrados.
    - Fluxos disponíveis para migração que ainda não foram migrados.
    - Fluxos não disponíveis para migração.
  - Identifica inconsistências, como fluxos marcados como migrados, mas que não estão disponíveis para migração.

- **Atualização Automática**:
  - O campo `Disponível para Migrar` no arquivo `controle_fluxos.csv` é atualizado automaticamente com base no status das dependências presentes nos arquivos `data.csv` e `fluxos.csv`.

- **Gerenciamento de Fluxos**:
  - Permite marcar fluxos como migrados diretamente na interface do sistema.

## Estrutura do Projeto

```plaintext
controle_migracao/
├── archives/
│   ├── data.csv                # Status das tabelas
│   ├── fluxos.csv              # Dependências dos fluxos
│   ├── controle_fluxos.csv     # Status dos fluxos
├── pages/
│   ├── 01_Migração_Tabelas.py  # Página para controle das tabelas que foram ou não migradas
│   ├── 02_Fluxos.py            # Página para gerenciar fluxos
├── config.py                   # Configurações e funções auxiliares
├── Dashboard.py                # Arquivo principal do dashboard
├── .gitignore                  # Arquivo para ignorar arquivos no Git
└── README.md                   # Documentação do projeto
```

## Pré-requisitos

- **Python**: Versão 3.8 ou superior.
- **Bibliotecas Necessárias**:
  - `streamlit`
  - `pandas`

Instale as dependências utilizando o comando:

```bash
pip install -r requirements.txt
```

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/BrunoAzeved/controle_migracao.git
   cd controle_migracao
   ```

2. Execute o dashboard:
   ```bash
   streamlit run Dashboard.py
   ```

Pronto! Agora você pode acessar o sistema no navegador e começar a gerenciar os fluxos de migração.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
