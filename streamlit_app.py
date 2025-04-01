import streamlit as st
from seguimiento_pre import app_pre
from seguimiento_vpd import app_vpd
from seguimiento_vpf import app_vpf  # 👈 Importa la nueva función

st.set_page_config(page_title="Seguimiento de Indicadores", layout="wide")
st.title("📊 Sistema de Seguimiento de Indicadores")

# Menú lateral
opcion = st.sidebar.radio("Seleccionar Área:", ["PRE", "VPD", "VPF"])  # 👈 Cambia el nombre en el menú

# Redireccionar según la opción
if opcion == "PRE":
    app_pre()
elif opcion == "VPD":
    app_vpd()
elif opcion == "VPF":
    app_vpf()

