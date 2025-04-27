import streamlit as st
import pandas as pd
import os
import config

# Configuração da página
st.set_page_config(
    page_title="Visão Geral dos fluxos e suas dependências", layout="wide"
)

# Configuração da logo
st.logo(config.LOGO_B3_NEGATIVO, size="large", icon_image=config.LOGO_B3_NEGATIVO)

# Verifica se os arquivos necessários existem
if not os.path.exists(config.FLUXOS_FILE) or not os.path.exists(config.CONTROLE_FILE):
    st.error("Os arquivos necessários não foram encontrados.")
    st.stop()

# Carrega os dados
fluxos_df = pd.read_csv(config.FLUXOS_FILE, sep=";")
controle_fluxos_df = pd.read_csv(config.CONTROLE_FILE, sep=";")

# Combina os dados de fluxos e controle para exibição
visao_geral_df = pd.merge(
    fluxos_df, controle_fluxos_df, left_on="fluxo", right_on="Fluxo", how="left"
)

# Exibe o título
st.title("Visão Geral dos fluxos e suas dependências")

# Filtros interativos
st.sidebar.header("Filtros")

# Filtro por fluxo (selectbox)
fluxo_selecionado = st.sidebar.selectbox(
    "Selecione um fluxo:", options=["Todos"] + list(visao_geral_df["fluxo"].unique())
)

# Filtro por dependência (selectbox)
dependencia_selecionada = st.sidebar.selectbox(
    "Selecione uma dependência:",
    options=["Todas"] + list(visao_geral_df["dependencia"].unique()),
)

# Aplica os filtros
df_filtrado = visao_geral_df.copy()

if fluxo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["fluxo"] == fluxo_selecionado]

if dependencia_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["dependencia"] == dependencia_selecionada]

# Exibe a tabela filtrada com colunas selecionadas
colunas_para_exibir = [
    "Tipo",
    "fluxo",
    "dependencia",
    "migrado",
    "Disponível para Migrar",
]
st.dataframe(df_filtrado[colunas_para_exibir])
