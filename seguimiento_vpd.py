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

    df["Fecha de Carga"] = pd.to_datetime(df["Fecha de Carga"].astype(str), errors="coerce")

    if "hitos_nuevos_vpd" not in st.session_state:
        st.session_state.hitos_nuevos_vpd = []

    excel_vacio = df.empty
    indicadores_existentes = df["Indicador"].dropna().unique().tolist()

    modo = "Crear un nuevo indicador"
    if not excel_vacio:
        modo = st.radio("¿Qué deseas hacer?", ["Registrar avance de indicador existente", "Crear un nuevo indicador"])

    trimestres = df["Trimestre"].dropna().unique().tolist() if not excel_vacio else ["I", "II", "III", "IV"]
    estados = df["Estado"].dropna().unique().tolist() if not excel_vacio else ["Por Comenzar", "En Proceso", "Finalizado"]

    st.subheader("📝 Formulario de Registro")

    with st.form("form_vpd"):
        # Área
        if modo == "Crear un nuevo indicador":
            area = st.text_input("Área")
        else:
            area = st.selectbox("Área", df["Area"].dropna().unique().tolist())

        if modo == "Crear un nuevo indicador":
            indicador = st.text_input("Nombre del nuevo Indicador")
            estrategico = st.text_input("IDEstrategico")
            anio_gestion = st.number_input("Año de Gestión", min_value=2020, max_value=2100, value=date.today().year)
            id_indicador = int(df["ID Indicador"].max()) + 1 if "ID Indicador" in df.columns and not df["ID Indicador"].isnull().all() else 1

            st.markdown("#### ➕ Añadir Hitos del Indicador")
            nuevo_hito = st.text_input("Escribe un hito y haz clic en Agregar")

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.form_submit_button("➕ Agregar Hito"):
                    if nuevo_hito.strip():
                        st.session_state.hitos_nuevos_vpd.append(nuevo_hito.strip())
            with col2:
                if st.form_submit_button("🗑 Limpiar Hitos"):
                    st.session_state.hitos_nuevos_vpd = []

            if st.session_state.hitos_nuevos_vpd:
                st.markdown("**Hitos agregados:**")
                for i, h in enumerate(st.session_state.hitos_nuevos_vpd, 1):
                    st.markdown(f"{i}. {h}")

        else:
            indicador = st.selectbox("Indicador", indicadores_existentes)
            df_ind = df[df["Indicador"] == indicador]
            anios = sorted(df_ind["Año"].dropna().unique().tolist())
            anio_gestion = st.selectbox("Año de Gestión", anios)
            df_anio = df_ind[df_ind["Año"] == anio_gestion]
            estrategico = df_anio["IDEstrategico"].values[0] if not df_anio.empty else ""
            id_indicador = df_anio["ID Indicador"].values[0] if not df_anio.empty else 1
            hitos_lista = df_anio["Hito"].dropna().unique().tolist()
            hito = st.selectbox("Hito", hitos_lista)

        trimestre = st.selectbox("Trimestre", trimestres)
        fecha_cierre = st.date_input("Fecha de Cierre", value=date(2025, 3, 27))

        if modo == "Registrar avance de indicador existente":
            avance_total = st.number_input("Avance Total (%)", min_value=0, max_value=100)
            estado = st.selectbox("Estado", estados)
        else:
            avance_total = 0
            estado = "Por Comenzar"

        # Responsable
        if modo == "Crear un nuevo indicador":
            responsable = st.text_input("Responsable")
        else:
            responsable = st.selectbox("Responsable", df["Responsable"].dropna().unique().tolist())

        submitted = st.form_submit_button("✅ Guardar")

    if submitted:
        if modo == "Crear un nuevo indicador":
            if not indicador or not estrategico or not st.session_state.hitos_nuevos_vpd or not area or not responsable:
                st.warning("⚠️ Completa todos los campos y agrega al menos un hito.")
                return

            nuevas_filas = []
            for i, h in enumerate(st.session_state.hitos_nuevos_vpd):
                nuevas_filas.append({
                    "Area": area,
                    "Indicador": indicador,
                    "IDEstrategico": estrategico,
                    "Año": anio_gestion,
                    "Orden Hito": i + 1,
                    "Trimestre": trimestre,
                    "Hito": h,
                    "Fecha de Cierre": fecha_cierre,
                    "Fecha de Carga": pd.to_datetime("2025-03-27"),
                    "Avance Total (%)": 0,
                    "Estado": "Por Comenzar",
                    "Responsable": responsable
                })

            df = pd.concat([df, pd.DataFrame(nuevas_filas)], ignore_index=True)
            st.session_state.hitos_nuevos_vpd = []
            st.success(f"✅ Se registraron {len(nuevas_filas)} hitos para el nuevo indicador '{indicador}'.")

        else:
            nueva_fila = {
                "Area": area,
                "Indicador": indicador,
                "IDEstrategico": estrategico,
                "Año": anio_gestion,
                "Orden Hito": 1,
                "Trimestre": trimestre,
                "Hito": hito,
                "Fecha de Cierre": fecha_cierre,
                "Fecha de Carga": pd.to_datetime("2025-03-27"),
                "Avance Total (%)": avance_total,
                "Estado": estado,
                "Responsable": responsable
            }

            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
            st.success(f"✅ Avance registrado para el indicador '{indicador}'.")

        df.to_excel(EXCEL_PATH, index=False, engine="openpyxl")

    st.subheader(f"📊 Historial de avances VPD – {anio_gestion}")
    st.dataframe(df[df["Año"] == anio_gestion].sort_values(by="Fecha de Carga", ascending=False))