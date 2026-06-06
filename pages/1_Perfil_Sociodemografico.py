import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==================================
# TÍTULO
# ==================================

st.title("Perfil Sociodemográfico")

st.write(
    """
    Evolução do perfil dos registros migratórios
    internacionais regularizados na Bahia
    entre 2021 e 2025.
    """
)

# ==================================
# LEITURA DOS DADOS
# ==================================

crescimento = pd.read_csv(
    "dados/crescimento_anual.csv"
)

sexo = pd.read_csv(
    "dados/sexo_ano.csv"
)

classificacao = pd.read_csv(
    "dados/classificacao_ano.csv"
)

heat_continente = pd.read_csv(
    "dados/heat_continente.csv"
)

heat_amparo = pd.read_csv(
    "dados/heat_amparo.csv"
)

heat_profissao = pd.read_csv(
    "dados/heat_profissao.csv"
)

# ==================================
# ABAS DOS GRÁFICOS DE LINHA
# ==================================

aba1, aba2, aba3 = st.tabs(
    [
        "📈 Evolução",
        "👨👩 Sexo",
        "📋 Classificação"
    ]
)

# ==================================
# EVOLUÇÃO
# ==================================

with aba1:

    st.subheader(
        "Evolução anual da frequência absoluta dos migrantes com registros migratórios na Bahia"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=crescimento["ano"],
            y=crescimento["migrantes"],
            mode="lines+markers+text",
            text=[
                f"{x:,}".replace(",", ".")
                for x in crescimento["migrantes"]
            ],
            textposition="top center",
            line=dict(
                color="#333795",
                width=5
            ),
            marker=dict(
                color="#B31D2D",
                size=12
            )
        )
    )

    fig.update_layout(
        height=600,
        template="simple_white",
        showlegend=False,
        xaxis_title="Ano",
        yaxis_title="Número de migrantes"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[2021, 2022, 2023, 2024, 2025]
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# SEXO
# ==================================

with aba2:

    st.subheader(
        "Evolução anual do sexo dos migrantes regularizados na Bahia"
    )

    cores = {
        "Masculino": "#333795",
        "Feminino": "#B31D2D",
        "Não especificado": "#F2B134"
    }

    fig = go.Figure()

    for sexo_cat in sexo["SEXO"].unique():

        dados = sexo[
            sexo["SEXO"] == sexo_cat
        ]

        fig.add_trace(
            go.Scatter(
                x=dados["ano"],
                y=dados["n"],
                mode="lines+markers+text",
                text=dados["n"],
                textposition="top center",
                name=sexo_cat,
                line=dict(
                    width=4,
                    color=cores.get(
                        sexo_cat,
                        "#444444"
                    )
                ),
                marker=dict(
                    size=10
                )
            )
        )

    fig.update_layout(
        height=600,
        template="simple_white",
        xaxis_title="Ano",
        yaxis_title="Número de migrantes",
        legend_title="Sexo"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[2021, 2022, 2023, 2024, 2025]
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# CLASSIFICAÇÃO
# ==================================

with aba3:

    st.subheader(
        "Evolução anual das classificações de situação migratória na Bahia"
    )

    cores_class = {
        "Temporário": "#333795",
        "Residente": "#B31D2D",
        "Provisório": "#F2B134"
    }

    fig = go.Figure()

    for categoria in classificacao[
        "CLASSIFICACAO_REGISTRO"
    ].unique():

        dados = classificacao[
            classificacao[
                "CLASSIFICACAO_REGISTRO"
            ] == categoria
        ]

        fig.add_trace(
            go.Scatter(
                x=dados["ano"],
                y=dados["n"],
                mode="lines+markers+text",
                text=dados["n"],
                textposition="top center",
                name=categoria,
                line=dict(
                    width=4,
                    color=cores_class.get(
                        categoria,
                        "#444444"
                    )
                ),
                marker=dict(
                    size=10
                )
            )
        )

    fig.update_layout(
        height=600,
        template="simple_white",
        xaxis_title="Ano",
        yaxis_title="Número de migrantes",
        legend_title="Classificação"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[2021, 2022, 2023, 2024, 2025]
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# SEPARADOR
# ==================================

st.markdown("---")

st.header("Distribuições Percentuais Anuais")

# ==================================
# ABAS DOS HEATMAPS
# ==================================

aba_h1, aba_h2, aba_h3 = st.tabs(
    [
        "🌎 Continente",
        "📄 Tipologia de Amparo",
        "💼 Profissão"
    ]
)

# ==================================
# PALETA
# ==================================

cores_heatmap = [
    [0.00, "#deebf7"],
    [0.25, "#9ecae1"],
    [0.50, "#3182bd"],
    [0.75, "#6a00a8"],
    [1.00, "#3f007d"]
]

# ==================================
# CONTINENTE
# ==================================

with aba_h1:

    st.subheader(
        "Distribuição percentual por continente de origem"
    )

    tabela = heat_continente.pivot(
        index="CONTINENTE",
        columns="ano",
        values="percentual"
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=tabela.values,
            x=tabela.columns,
            y=tabela.index,
            colorscale=cores_heatmap,
            text=np.round(tabela.values, 1),
            texttemplate="%{text}%",
            colorbar_title="%"
        )
    )

    fig.update_layout(
        height=500,
        template="simple_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# AMPARO
# ==================================

with aba_h2:

    st.subheader(
        "Distribuição percentual por tipologia de amparo"
    )

    tabela = heat_amparo.pivot(
        index="TIPOLOGIA_AMPAROS",
        columns="ano",
        values="percentual"
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=tabela.values,
            x=tabela.columns,
            y=tabela.index,
            colorscale=cores_heatmap,
            text=np.round(tabela.values, 1),
            texttemplate="%{text}%",
            colorbar_title="%"
        )
    )

    fig.update_layout(
        height=650,
        template="simple_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# PROFISSÃO
# ==================================

with aba_h3:

    st.subheader(
        "Distribuição percentual por grupo profissional"
    )

    tabela = heat_profissao.pivot(
        index="grupo_profissao",
        columns="ano",
        values="percentual"
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=tabela.values,
            x=tabela.columns,
            y=tabela.index,
            colorscale=cores_heatmap,
            text=np.round(tabela.values, 1),
            texttemplate="%{text}%",
            colorbar_title="%"
        )
    )

    fig.update_layout(
        height=650,
        template="simple_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
