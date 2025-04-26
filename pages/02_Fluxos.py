import streamlit as st
import pandas as pd
import os
import config  # Importa o arquivo de configuração
import time

# Verifica se os arquivos necessários existem
if not os.path.exists(config.DATA_FILE) or not os.path.exists(config.FLUXOS_FILE):
    st.error("Os arquivos necessários não foram encontrados.")
    st.stop()

# Carrega os dados
data_df = pd.read_csv(config.DATA_FILE)
fluxos_df = pd.read_csv(config.FLUXOS_FILE)
controle_fluxos_df = pd.read_csv(config.ARCHIVES_DIR + "/controle_fluxos.csv")

# Função para verificar se todas as dependências de um fluxo estão prontas
def is_fluxo_ready(fluxo, data_df, fluxos_df):
    dependencias = fluxos_df[fluxos_df["fluxo"] == fluxo]["dependencia"]
    return all(data_df[data_df["tabela_op"].isin(dependencias)]["pronta"])

# Identifica fluxos prontos para migração
fluxos_prontos = [
    fluxo for fluxo in fluxos_df["fluxo"].unique()
    if is_fluxo_ready(fluxo, data_df, fluxos_df)
]

# Atualiza o DataFrame de controle com o status de disponibilidade para migração
controle_fluxos_df["Disponível para Migrar"] = controle_fluxos_df["Fluxo"].apply(
    lambda fluxo: "Sim" if fluxo in fluxos_prontos else "Não"
)

# Exibe fluxos prontos para migração em formato de tabela
st.title("Fluxos Prontos para Migração")

if not controle_fluxos_df.empty:
    st.subheader("Tabela de Fluxos")
    edited_fluxos_df = st.data_editor(
        controle_fluxos_df,
        column_config={
            "Fluxo": st.column_config.TextColumn(label="Fluxo", width="large"),
            "migrado": st.column_config.CheckboxColumn(
                label="Migrado",
                help="Indica se o fluxo foi migrado"
            ),
            "Disponível para Migrar": st.column_config.TextColumn(label="Disponível para Migrar", width="small", disabled=True),
        },
        hide_index=True,
        num_rows="dynamic"
    )

    # Atualiza o status de migração com base nas edições feitas pelo usuário
    if st.sidebar.button("Salvar Alterações"):
        edited_fluxos_df.to_csv(config.CONTROLE_FILE, index=False)
        st.sidebar.success("Alterações salvas com sucesso!")
        config.atualizar_disponibilidade_para_migrar()
        time.sleep(2)
        st.rerun()
    
    # Verifica se existem alterações não salvas
    if not controle_fluxos_df.equals(edited_fluxos_df):
        st.sidebar.warning("Existem alterações não salvas na tabela de fluxos!")

else:
    st.info("Nenhum fluxo está disponível para exibição.")