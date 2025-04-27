import streamlit as st
import pandas as pd
import os
import time
import config  # Importa o arquivo de configuração


# Configuração da página
st.set_page_config(layout="wide")

# Configuração da logo
st.logo(config.LOGO_B3_NEGATIVO, size="large", icon_image=config.LOGO_B3_NEGATIVO)

# Verifica se o diretório de arquivos existe, caso contrário, cria o diretório
if not os.path.exists(config.ARCHIVES_DIR):
    os.makedirs(config.ARCHIVES_DIR)

st.title("Controle Migração")

data_df = pd.read_csv(config.DATA_FILE, parse_dates=["data_prevista"], sep=";")

edited_df = st.data_editor(
    data_df,
    column_config={
        "data_prevista": st.column_config.DateColumn(
            label="Data Prevista",
            pinned=True,
            width="large",
        ),
        "rating": st.column_config.NumberColumn(
            label="Rating",
            min_value=0,
            max_value=5,
            step=1,
            format="%d ⭑",
            help="Avaliação do arquivo",
            width="small",
        ),
    },
    num_rows="dynamic",
    hide_index=False,
)

if st.sidebar.button("Salvar Alterações"):
    data_df = edited_df
    data_df.to_csv(config.DATA_FILE, index=False)
    st.sidebar.success("Alterações salvas com sucesso!")
    config.atualizar_disponibilidade_para_migrar()
    time.sleep(2)
    st.rerun()

# Verifica se existem alterações não salvas
if not data_df.equals(edited_df):
    st.sidebar.warning("Existem alterações não salvas!")
