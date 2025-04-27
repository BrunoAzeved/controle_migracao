import streamlit as st
import pandas as pd
import os
import config

# Configuração da página
st.set_page_config(page_title="Visão Geral dos Fluxos", layout="wide")

# Verifica se os arquivos necessários existem
if not os.path.exists(config.FLUXOS_FILE) or not os.path.exists(config.CONTROLE_FILE):
    st.error("Os arquivos necessários não foram encontrados.")
    st.stop()

# Carrega os dados
fluxos_df = pd.read_csv(config.FLUXOS_FILE)
controle_fluxos_df = pd.read_csv(config.CONTROLE_FILE)

# Combina os dados de fluxos e controle para exibição
visao_geral_df = pd.merge(
    fluxos_df, controle_fluxos_df, left_on="fluxo", right_on="Fluxo", how="left"
)

# Filtros interativos
st.sidebar.header("Filtros")
status_migrado = st.sidebar.multiselect(
    "Status de Migração",
    options=["Sim", "Não"],
    default=["Sim", "Não"],
    key="migrado_filter",
)

status_disponivel = st.sidebar.multiselect(
    "Disponível para Migrar",
    options=["Sim", "Não"],
    default=["Sim", "Não"],
    key="disponivel_filter",
)

# Aplica os filtros
filtered_df = visao_geral_df[
    (visao_geral_df["migrado"].isin(status_migrado))
    & (visao_geral_df["Disponível para Migrar"].isin(status_disponivel))
]

# Exibe a tabela filtrada
st.title("Visão Geral dos Fluxos")
if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("Nenhum fluxo encontrado com os filtros selecionados.")

# Exibe as dependências de um fluxo selecionado
st.subheader("Dependências de Fluxos")
fluxo_selecionado = st.selectbox(
    "Selecione um Fluxo para visualizar as dependências:",
    options=fluxos_df["fluxo"].unique(),
    key="fluxo_dependencia",
)

dependencias = fluxos_df[fluxos_df["fluxo"] == fluxo_selecionado]["dependencia"]
if not dependencias.empty:
    st.write(f"Dependências do fluxo **{fluxo_selecionado}**:")
    st.write(dependencias.tolist())
else:
    st.write(f"O fluxo **{fluxo_selecionado}** não possui dependências.")