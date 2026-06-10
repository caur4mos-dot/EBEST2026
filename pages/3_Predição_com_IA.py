import streamlit as st
import geopandas as gpd
import folium

from branca.colormap import LinearColormap
from streamlit_folium import st_folium

# =========================
# TÍTULO
# =========================

st.title("Predição dos Fluxos Migratórios para 2026")

st.write(
    """
    O mapa apresenta a taxa prevista de migrantes
    internacionais regularizados por 100 mil habitantes
    nas microrregiões da Bahia para o ano de 2026,
    estimada por modelo Random Forest.
    """
)

# =========================
# LEITURA DO GEOJSON
# =========================

mapa_2026 = gpd.read_file(
    "dados/mapa_predicao_2026.geojson"
)

# =========================
# LIMITES DA ESCALA
# =========================

taxa_min = mapa_2026["taxa_prevista_2026"].min()

taxa_max = mapa_2026["taxa_prevista_2026"].max()

# =========================
# PALETA IGUAL AO R
# =========================

colormap = LinearColormap(
    colors=[
        "grey95",
        "yellow",
        "#F5E400",
        "orange",
        "red"
    ],
    vmin=taxa_min,
    vmax=taxa_max
)

colormap.caption = "Taxa Prevista por 100 mil habitantes"

# =========================
# CENTRO DO MAPA
# =========================

centro = [
    mapa_2026.geometry.centroid.y.mean(),
    mapa_2026.geometry.centroid.x.mean()
]

# =========================
# MAPA
# =========================

m = folium.Map(
    location=centro,
    zoom_start=6,
    tiles="CartoDB positron"
)

# =========================
# CAMADA GEOJSON
# =========================

folium.GeoJson(
    mapa_2026,

    style_function=lambda feature: {

        "fillColor":
            "white"
            if (
                feature["properties"]["taxa_prevista_2026"] == 0
                or feature["properties"]["taxa_prevista_2026"] is None
            )
            else colormap(
                feature["properties"]["taxa_prevista_2026"]
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

        localize=True,

        sticky=False
    )

).add_to(m)

# =========================
# LEGENDA
# =========================

colormap.add_to(m)

# =========================
# EXIBIR
# =========================

st_folium(
    m,
    use_container_width=True,
    height=700
)
