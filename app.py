import streamlit as st

st.set_page_config(
    page_title="Análise temporal, espacial e sociodemográfica da migração internacional regularizada na Bahia entre 2021 e 2025 utilizando Inteligência Artificial para predição de 2026",
    page_icon="🌎",
    layout="wide"
)

st.title("Análise temporal, espacial e sociodemográfica da migração internacional regularizada na Bahia entre 2021 e 2025 utilizando Inteligência Artificial para predição de 2026")

st.markdown("""
Este site apresenta análises dos fluxos migratórios internacionais regularizados
na Bahia utilizando dados do SISMIGRA com o objetivo de compreender os padrões migratórios e apoiar a gestão da Bahia no fortalecimento de políticas públicas de acolhimento,
regularização documental, inclusão social, emprego, educação e planejamento territorial. Se alinhando a lei de Migração n° 13.445/2017 e ao Objetivo de Desenvolvimento Sustentável
(ODS) 10.7, que prevê a facilitaçãode uma migração segura e regular, e o ODS 16, que enfatiza instituições eficazes e acesso à justiça.


### Seções

- Perfil Sociodemográfico
- Visualização Espacial
- Predição dos Fluxos Migratórios
""")

import streamlit as st

st.set_page_config(
    page_title="Migração Internacional na Bahia",
    layout="wide"
)

st.title("")

st.markdown("""

""")

st.markdown("---")

# Criando 3 colunas, uma para cada imagem
col1, col2, col3 = st.columns(3)

with col1:
    # Mostra a primeira imagem (ajuste o nome se necessário)
    st.image("Design sem nome(6).png", width=150)

with col2:
    # Mostra a imagem da ODS 16
    st.image("Objetivo_Desenvolvimento_Sustentável_16_PT.jpg", width=150)

with col3:
    # Mostra a imagem da ODS 10
    st.image("SDG-icon-PT-RGB-10-1.jpg", width=150)
