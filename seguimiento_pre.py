import streamlit as st
import pandas as pd
from datetime import date
import os

EXCEL_PATH = "data/seguimiento_pre.xlsx"

def app_pre():
    st.header("📋 Seguimiento de Indicadores - Área PRE")

    if os.path.exists(EXCEL_PATH):
        df = pd.read_excel(EXCEL_PATH)
    else:
        st.error("No se encontró el archivo seguimiento_pre.xlsx")
        return

    # Conversión segura de fechas
    df["Fecha de Carga"] = pd.to_datetime(df["Fecha de Carga"].astype(str), errors="coerce")

    # Opciones únicas desde el Excel
    areas = df["Area"].dropna().unique().tolist()
    indicadores = df["Indicador"].dropna().unique().tolist()
    trimestres = df["Trimestre"].dropna().unique().tolist()
    hitos = df["Hito"].dropna().unique().tolist()
    estados = df["Estado"].dropna().unique().tolist()
    responsables = df["Responsable"].dropna().unique().tolist()

    st.subheader("📝 Registrar nuevo avance")

    with st.form("form_pre"):
        area = st.selectbox("Área", areas)
        indicador = st.selectbox("Indicador", indicadores)
        anio = st.number_input("Año", min_value=2020, max_value=2100, value=2025)
        trimestre = st.selectbox("Trimestre", trimestres)
        hito = st.selectbox("Hito", hitos)
        fecha_cierre = st.date_input("Fecha de Cierre", value=date(2025, 3, 27))
        avance_mensual = st.number_input("Avance Mensual (%)", min_value=0, max_value=100)
        avance_total = st.number_input("Avance Total (%)", min_value=0, max_value=100)
        estado = st.selectbox("Estado", estados)
        responsable = st.selectbox("Responsable", responsables)

        submitted = st.form_submit_button("Guardar")

    if submitted:
        # Buscar valores automáticos desde el Excel
        fila_existente = df[df["Indicador"] == indicador].head(1)
        id_indicador = fila_existente["ID Indicador"].values[0] if not fila_existente.empty else None
        estrategico = fila_existente["Indicador Estratégico"].values[0] if not fila_existente.empty else ""
        orden_hito = fila_existente["Orden Hito"].values[0] if not fila_existente.empty else None

        nueva_fila = {
            "Area": area,
            "Indicador": indicador,
            "Año": anio,
            "Trimestre": trimestre,
            "Hito": hito,
            "ID Indicador": id_indicador,
            "Indicador Estratégico": estrategico,
            "Fecha de Cierre": fecha_cierre,
            "Fecha de Carga": pd.to_datetime("2025-03-27"),
            "Avance Mensual (%)": avance_mensual,
            "Avance Total (%)": avance_total,
            "Estado": estado,
            "Responsable": responsable,
            "Orden Hito": orden_hito
        }

        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_excel(EXCEL_PATH, index=False)
        st.success("✅ Registro guardado exitosamente")

    st.subheader("📊 Historial de avances PRE")
    st.dataframe(df.sort_values(by="Fecha de Carga", ascending=False))

