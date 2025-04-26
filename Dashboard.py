import streamlit as st
import config
import pandas as pd


# Configuração da página
st.set_page_config(
    page_title="Dashboard de Migração",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Configuração da logo
st.logo(config.LOGO_B3_NEGATIVO, size="large", icon_image=config.LOGO_B3_NEGATIVO)

st.header("Dashboard de Controle de Migração")

# Atualiza o campo "Disponível para Migrar" antes de carregar os dados
config.atualizar_disponibilidade_para_migrar()

# Carrega os dados
df_migrados = pd.read_csv(config.CONTROLE_FILE)

# Verifica inconsistências: fluxos não disponíveis marcados como migrados
fluxos_inconsistentes = df_migrados[
    (df_migrados["Disponível para Migrar"] == "Não") & df_migrados["migrado"]
]

# Exibe um warning se houver fluxos inconsistentes
if not fluxos_inconsistentes.empty:
    st.warning(
        f"Existem {len(fluxos_inconsistentes)} fluxos marcados como migrados, "
        "mas que não estão disponíveis para migração. Verifique os dados!"
    )

# Calcula as métricas
total_fluxos = len(df_migrados)
fluxos_migrados = len(df_migrados[df_migrados["migrado"]])
fluxos_nao_migrados = len(df_migrados[~df_migrados["migrado"]])
fluxos_disponiveis_para_migrar = len(
    df_migrados[
        (df_migrados["Disponível para Migrar"] == "Sim") & ~df_migrados["migrado"]
    ]
)
fluxos_nao_disponiveis = len(
    df_migrados[df_migrados["Disponível para Migrar"] == "Não"]
)

# Exibe as métricas no dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Fluxos Migrados",
        value=fluxos_migrados,
        delta=f"{fluxos_migrados} de {total_fluxos}",
    )

with col2:
    st.metric(
        label="Fluxos Não Migrados",
        value=fluxos_nao_migrados,
        delta=f"{fluxos_nao_migrados} de {total_fluxos}",
    )

with col3:
    st.metric(
        label="Disponíveis para Migrar",
        value=fluxos_disponiveis_para_migrar,
    )

with col4:
    st.metric(
        label="Não Disponíveis para Migrar",
        value=fluxos_nao_disponiveis,
    )

st.dataframe(df_migrados)
