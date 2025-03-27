import streamlit as st
import pandas as pd
from datetime import date
import os

EXCEL_PATH = "data/seguimiento_vpd.xlsx"

def app_vpd():
    st.header("📋 Seguimiento de Indicadores - Área VPD")

    if os.path.exists(EXCEL_PATH):
        df = pd.read_excel(EXCEL_PATH)
    else:
        st.error("No se encontró el archivo seguimiento_vpd.xlsx")
        return

    # Conversión segura de fechas
    df["Fecha de Carga"] = pd.to_datetime(df["Fecha de Carga"].astype(str), errors="coerce")

    # Opciones para campos manuales
    indicadores = df["Indicador"].dropna().unique().tolist()
    trimestres = df["Trimestre"].dropna().unique().tolist()
    hitos = df["Hito"].dropna().unique().tolist()
    estados = df["Estado"].dropna().unique().tolist()
    responsables = df["Responsable"].dropna().unique().tolist()

    st.subheader("📝 Registrar nuevo avance")

    with st.form("form_vpd"):
        indicador = st.selectbox("Indicador", indicadores)
        trimestre = st.selectbox("Trimestre", trimestres)
        hito = st.selectbox("Hito", hitos)
        fecha_cierre = st.date_input("Fecha de Cierre", value=date(2025, 3, 27))
        avance_total = st.number_input("Avance Total (%)", min_value=0, max_value=100)
        estado = st.selectbox("Estado", estados)
        responsable = st.selectbox("Responsable", responsables)

        submitted = st.form_submit_button("Guardar")

    if submitted:
        # Buscar valores automáticos desde el Excel
        fila_existente = df[df["Indicador"] == indicador].head(1)
        estrategico = fila_existente["IDEstrategico"].values[0] if not fila_existente.empty else ""
        orden_hito = fila_existente["Orden Hito"].values[0] if not fila_existente.empty else None

        nueva_fila = {
            "Indicador": indicador,
            "IDEstrategico": estrategico,
            "Orden Hito": orden_hito,
            "Trimestre": trimestre,
            "Hito": hito,
            "Fecha de Cierre": fecha_cierre,
            "Fecha de Carga": pd.to_datetime("2025-03-27"),
            "Avance Total (%)": avance_total,
            "Estado": estado,
            "Responsable": responsable
        }

        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_excel(EXCEL_PATH, index=False, engine="openpyxl")
        st.success("✅ Registro guardado exitosamente")

    st.subheader("📊 Historial de avances VPD")
    st.dataframe(df.sort_values(by="Fecha de Carga", ascending=False))

