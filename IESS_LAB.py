# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.


"""
import streamlit as st
import pandas as pd
import plotly.express as px
 
# 1. Configuración de página
st.set_page_config(page_title="Dashboard Ejecutivo IESS", layout="wide")

# 2. Estilo Visual IESS (Azul Marino y Gris Ejecutivo)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { border-left: 5px solid #003366; background-color: white; padding: 10px; box-shadow: 2px 2px 5px #ccc; }
    h1 { color: #003366; }
    </style>
    """, unsafe_allow_html=True)

# 3. Carga de datos optimizada
@st.cache_data
def load_data():
    file = "distributivo COMPLETO ENVIAR 19-02-2026_para informacion.xlsx"
    # Cargamos la hoja 'base' usando el motor openpyxl
    df = pd.read_excel(file, sheet_name='base', engine='openpyxl')
    return df

try:
    df = load_data()

    st.title("🏛️ Análisis Estadístico de Talento Humano - IESS")
    st.markdown("---")

    # 4. BARRA LATERAL CON LOS 7 FILTROS SOLICITADOS
    st.sidebar.header("Filtros de Control")
    
    # Filtro 1: Género
    f_genero = st.sidebar.multiselect("Género", options=df["GENERO"].unique(), default=df["GENERO"].unique())
    # Filtro 2: Grado Salarial
    f_grado = st.sidebar.multiselect("Grado Salarial", options=sorted(df["GRADO_SALARIAL"].unique()), default=df["GRADO_SALARIAL"].unique())
    # Filtro 3: Provincia
    f_prov = st.sidebar.multiselect("Provincia", options=df["PROVINCIA"].unique(), default=df["PROVINCIA"].unique())
    # Filtro 4: Contratos NSJ
    f_nsj = st.sidebar.multiselect("Contratos NSJ", options=df["contratos NSJ"].unique(), default=df["contratos NSJ"].unique())
    # Filtro 5: Nivel Jerárquico Superior
    f_njs = st.sidebar.multiselect("Nivel Jerárquico Superior", options=df["NIVEL JERARQUICO SUPERIOR"].unique(), default=df["NIVEL JERARQUICO SUPERIOR"].unique())
    # Filtro 6: Modalidad
    f_mod = st.sidebar.multiselect("Modalidad", options=df["Modalidad"].unique(), default=df["Modalidad"].unique())
    # Filtro 7: Régimen
    f_reg = st.sidebar.multiselect("Régimen", options=df["REGIMEN"].unique(), default=df["REGIMEN"].unique())

    # Aplicación de filtros en cascada
    mask = (df["GENERO"].isin(f_genero)) & \
           (df["GRADO_SALARIAL"].isin(f_grado)) & \
           (df["PROVINCIA"].isin(f_prov)) & \
           (df["contratos NSJ"].isin(f_nsj)) & \
           (df["NIVEL JERARQUICO SUPERIOR"].isin(f_njs)) & \
           (df["Modalidad"].isin(f_mod)) & \
           (df["REGIMEN"].isin(f_reg))
    
    df_f = df[mask]

    # 5. KPIS PRINCIPALES
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Población Filtrada", f"{len(df_f):,}")
    with c2:
        st.metric("Masa Salarial (RMU)", f"${df_f['SALARIO_BASE'].sum():,.2f}")
    with c3:
        st.metric("Promedio Salarial", f"${df_f['SALARIO_BASE'].mean():,.2f}")

    # 6. GRÁFICOS SOLICITADOS
    st.markdown("### Visualización de Estructura Laboral")
    g1, g2 = st.columns(2)

    with g1:
        # Gráfico por Régimen Laboral
        fig_reg = px.pie(df_f, names='REGIMEN', title="Composición por Régimen", hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_reg, use_container_width=True)

    with g2:
        # Gráfico por Grado Salarial (Frecuencia)
        fig_grad = px.bar(df_f['GRADO_SALARIAL'].value_counts().reset_index(), 
                          x='GRADO_SALARIAL', y='count', title="Distribución por Grado Salarial",
                          labels={'count': 'Servidores', 'GRADO_SALARIAL': 'Grado'},
                          color_discrete_sequence=['#003366'])
        st.plotly_chart(fig_grad, use_container_width=True)

    # Gráfico de Modalidad vs Presupuesto
    fig_mod = px.box(df_f, x="Modalidad", y="SALARIO_BASE", color="GENERO",
                     title="Distribución Salarial por Modalidad y Género",
                     color_discrete_map={'FEMENINO': '#6b8fb4', 'MASCULINO': '#003366'})
    st.plotly_chart(fig_mod, use_container_width=True)

    # 7. TABLA DE DATOS PARA AUDITORÍA
    with st.expander("Ver Datos Depurados"):
        st.dataframe(df_f)

except Exception as e:
    st.error(f"Error detectado: {e}")
    st.info("Verifica que el archivo '.xlsx' esté en la misma carpeta que este script.")