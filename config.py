import pandas as pd
import os


# Caminhos dos arquivos
ARCHIVES_DIR = "archives"
DATA_FILE = os.path.join(ARCHIVES_DIR, "data.csv")
FLUXOS_FILE = os.path.join(ARCHIVES_DIR, "fluxos.csv")
CONTROLE_FILE = os.path.join(ARCHIVES_DIR, "controle_fluxos.csv")

# Configuração da logo
LOGO_B3_NEGATIVO = "images/logo_b3_negativo.png"


# Função para atualizar o campo "Disponível para Migrar" no controle_fluxos.csv
def atualizar_disponibilidade_para_migrar():
    """
    Atualiza o campo 'Disponível para Migrar' no arquivo controle_fluxos.csv
    com base no status das dependências em data.csv e fluxos.csv.
    """
    # Verifica se os arquivos necessários existem
    if (
        not os.path.exists(DATA_FILE)
        or not os.path.exists(FLUXOS_FILE)
        or not os.path.exists(CONTROLE_FILE)
    ):
        raise FileNotFoundError(
            "Um ou mais arquivos necessários não foram encontrados."
        )

    # Carrega os dados
    data_df = pd.read_csv(DATA_FILE, sep=";")
    fluxos_df = pd.read_csv(FLUXOS_FILE, sep=";")
    controle_fluxos_df = pd.read_csv(CONTROLE_FILE, sep=";")

    # Função para verificar se todas as dependências de um fluxo estão prontas
    def is_fluxo_ready(fluxo):
        dependencias = fluxos_df[fluxos_df["fluxo"] == fluxo]["dependencia"]
        return all(data_df[data_df["tabela_op"].isin(dependencias)]["pronta"])

    # Atualiza o campo 'Disponível para Migrar'
    controle_fluxos_df["Disponível para Migrar"] = controle_fluxos_df["Fluxo"].apply(
        lambda fluxo: "Sim" if is_fluxo_ready(fluxo) else "Não"
    )

    # Salva as alterações no arquivo controle_fluxos.csv
    controle_fluxos_df.to_csv(CONTROLE_FILE, index=False, sep=";")
