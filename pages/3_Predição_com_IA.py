import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import plotly.express as px

from branca.colormap import LinearColormap
from streamlit_folium import st_folium

# =====================================================
# TÍTULO
# =====================================================

st.title("Predição dos Fluxos Migratórios para 2026")

st.write(
    """
    Esta seção apresenta a predição da taxa de migrantes
    internacionais regularizados por 100 mil habitantes
    nas microrregiões da Bahia para o ano de 2026.

    As estimativas foram produzidas por um modelo de
    Random Forest treinado a partir dos padrões observados
    entre 2021 e 2025.
    """
)

# =====================================================
# LEITURA DOS DADOS
# =====================================================

mapa_2026 = gpd.read_file(
    "dados/mapa_predicao_2026.geojson"
)

metricas = pd.read_csv(
    "dados/metricas_validacao.csv"
)

validacao = pd.read_csv(
    "dados/validacao_2025.csv"
)

# =====================================================
# TOP 5 MICRORREGIÕES PREVISTAS
# =====================================================

st.subheader(
    "Microrregiões com maiores taxas previstas para 2026"
)

top5 = (
    mapa_2026[
        ["name_micro", "taxa_prevista_2026"]
    ]
    .sort_values(
        "taxa_prevista_2026",
        ascending=False
    )
    .head(5)
)

top5.columns = [
    "Microrregião",
    "Taxa Prevista (2026)"
]

st.dataframe(
    top5,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# MAPA INTERATIVO
# =====================================================

st.subheader(
    "Mapa Interativo da Predição para 2026"
)

taxa_min = 0
taxa_max = 40

colormap = LinearColormap(
    colors=[
        "#F2F2F2",
        "#FFFF00",
        "#F5E400",
        "#FFA500",
        "#FF0000"
    ],
    vmin=taxa_min,
    vmax=taxa_max
)

colormap.caption = (
    "Taxa Prevista por 100 mil habitantes"
)

centro = [
    mapa_2026.geometry.centroid.y.mean(),
    mapa_2026.geometry.centroid.x.mean()
]

m = folium.Map(
    location=centro,
    zoom_start=6,
    tiles="CartoDB positron"
)

folium.GeoJson(
    mapa_2026,

    style_function=lambda feature: {

        "fillColor":
            "white"
            if (
                feature["properties"][
                    "taxa_prevista_2026"
                ] == 0
                or feature["properties"][
                    "taxa_prevista_2026"
                ] is None
            )
            else colormap(
                feature["properties"][
                    "taxa_prevista_2026"
                ]
            ),

        "color": "black",

        "weight": 1,

        "fillOpacity": 1
    },

    tooltip=folium.GeoJsonTooltip(

        fields=[
            "name_micro",
            "taxa_prevista_2026"
        ],

        aliases=[
            "Microrregião:",
            "Taxa Prevista 2026:"
        ],

        localize=True
    )

).add_to(m)

colormap.add_to(m)

st_folium(
    m,
    use_container_width=True,
    height=700
)

# =====================================================
# VALIDAÇÃO
# =====================================================

st.divider()

st.header(
    "Validação do Modelo"
)

st.write(
    """
    Antes da realização da predição para 2026,
    o modelo foi validado utilizando os dados
    observados em 2025.

    Para isso, os registros históricos anteriores
    foram utilizados para prever as taxas de migração
    de 2025, permitindo comparar os valores previstos
    com os valores efetivamente observados.
    """
)

# =====================================================
# MÉTRICAS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Erro Absoluto Médio",
        f"{metricas['MAE'][0]:.2f}"
    )

with col2:
    st.metric(
        "Erro Percentual Médio",
        f"{metricas['MAPE'][0]:.1f}%"
    )

with col3:
    st.metric(
        "Correlação",
        f"{metricas['CORRELACAO'][0]:.2f}"
    )

# =====================================================
# GRÁFICO REAL X PREVISTO
# =====================================================

st.subheader(
    "Comparação entre valores reais e previstos"
)

fig = px.scatter(
    validacao,
    x="taxa_100k",
    y="taxa_prevista",
    hover_name="name_micro"
)

valor_max = max(
    validacao["taxa_100k"].max(),
    validacao["taxa_prevista"].max()
)

fig.add_shape(
    type="line",
    x0=0,
    y0=0,
    x1=valor_max,
    y1=valor_max
)

fig.update_layout(
    xaxis_title="Taxa Real",
    yaxis_title="Taxa Prevista",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TABELA COMPLETA
# =====================================================

st.subheader(
    "Tabela completa de validação"
)

st.dataframe(
    validacao.sort_values(
        "taxa_prevista",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)
