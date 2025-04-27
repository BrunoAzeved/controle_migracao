import streamlit as st
import config
import pandas as pd
import plotly.express as px


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
data_df = pd.read_csv(config.DATA_FILE)
fluxos_df = pd.read_csv(config.FLUXOS_FILE)

# Verifica inconsistências: fluxos não disponíveis marcados como migrados
fluxos_inconsistentes = df_migrados[
    (df_migrados["Disponível para Migrar"] == "Não") & df_migrados["migrado"]
]

# Identifica tabelas que não foram migradas e que deveriam estar prontas
dependencias_inconsistentes = fluxos_df[
    fluxos_df["fluxo"].isin(fluxos_inconsistentes["Fluxo"])
]["dependencia"]

tabelas_nao_migradas = data_df[
    (data_df["tabela_op"].isin(dependencias_inconsistentes)) & (~data_df["pronta"])
]

# Exibe um warning se houver fluxos inconsistentes
if not fluxos_inconsistentes.empty:
    num_fluxos_inconsistentes = len(fluxos_inconsistentes)
    if num_fluxos_inconsistentes == 1:
        st.warning(
            f"Existe {num_fluxos_inconsistentes} fluxo marcado como migrado, "
            "mas que não está disponível para migração. Verifique os dados!"
        )
    else:
        st.warning(
            f"Existem {num_fluxos_inconsistentes} fluxos marcados como migrados, "
            "mas que não estão disponíveis para migração. Verifique os dados!"
        )

    # Campo expansível para exibir detalhes
    with st.expander("Detalhes das Inconsistências"):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Fluxos Marcados como Migrados (Inconsistentes)")
            st.write(fluxos_inconsistentes[["Fluxo", "data_migracao"]])

        with col2:
            st.subheader("Tabelas Não Migradas")
            st.write(tabelas_nao_migradas[["tabela_op", "data_prevista"]])

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
    st.metric(label="Disponíveis para Migrar", value=fluxos_disponiveis_para_migrar)

with col4:
    st.metric(label="Processos Aguardando Liberação", value=fluxos_nao_disponiveis)

percentual_migrados = (fluxos_migrados / total_fluxos) * 100 if total_fluxos > 0 else 0
st.metric(
    label="Percentual de Fluxos Migrados",
    value=f"{percentual_migrados:.2f}%",
)

fluxos_disponiveis = df_migrados[
    (df_migrados["Disponível para Migrar"] == "Sim") & ~df_migrados["migrado"]
]
with st.expander("Fluxos Disponíveis para Migração"):
    st.write(fluxos_disponiveis[["Fluxo", "Disponível para Migrar"]])

historico_migrados = df_migrados[df_migrados["migrado"]][["Fluxo", "data_migracao"]]
with st.expander("Histórico de Fluxos Migrados"):
    st.write(historico_migrados)

data_df["data_prevista"] = pd.to_datetime(data_df["data_prevista"], errors="coerce")
tabelas_atrasadas = data_df[
    (data_df["data_prevista"] < pd.Timestamp.now()) & (~data_df["pronta"])
]
with st.expander("Tabelas com Atraso"):
    st.write(tabelas_atrasadas[["tabela_op", "data_prevista"]])

tabelas_mais_dependentes = fluxos_df["dependencia"].value_counts()
tabelas_nao_migradas_dependentes = tabelas_mais_dependentes[
    tabelas_mais_dependentes.index.isin(tabelas_nao_migradas["tabela_op"])
]
with st.expander("Tabelas Mais Dependentes (Não Migradas)"):
    st.write(tabelas_nao_migradas_dependentes)

status_fluxos = pd.DataFrame(
    {
        "Status": [
            "Migrados",
            "Não Migrados",
            "Disponíveis para Migrar",
            "Não Disponíveis",
        ],
        "Quantidade": [
            fluxos_migrados,
            fluxos_nao_migrados,
            fluxos_disponiveis_para_migrar,
            fluxos_nao_disponiveis,
        ],
    }
)

fig = px.pie(
    status_fluxos, names="Status", values="Quantidade", title="Distribuição dos Fluxos"
)
st.plotly_chart(fig)
