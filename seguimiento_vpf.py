import streamlit as st
import pandas as pd

def app_vpf():
    st.title("📥 Seguimiento de Indicadores - VPF")

    archivo = st.file_uploader("Selecciona el archivo Excel", type=["xlsx"])

    if archivo is not None:
        try:
            # Leer todas las hojas
            excel_data = pd.read_excel(archivo, sheet_name=None)
            hojas = list(excel_data.keys())

            # Elegir hoja
            area = st.selectbox("Selecciona el Área (nombre de la hoja):", hojas)
            df = excel_data[area]

            # Verificar si hay datos válidos
            if not df.empty and df.shape[1] > 1:
                st.success(f"Datos cargados del área: {area}")
                st.subheader("Vista previa de los datos:")
                st.dataframe(df, use_container_width=True)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("💾 Guardar como CSV"):
                        nombre_csv = f"{area.lower().replace(' ', '_')}.csv"
                        df.to_csv(nombre_csv, index=False)
                        st.success(f"Guardado como {nombre_csv}")

                with col2:
                    if st.button("💾 Guardar como Parquet"):
                        nombre_parquet = f"{area.lower().replace(' ', '_')}.parquet"
                        df.to_parquet(nombre_parquet, index=False)
                        st.success(f"Guardado como {nombre_parquet}")
            else:
                st.warning("⚠️ La hoja seleccionada no contiene suficientes datos válidos.")

        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {e}")
