import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import os

def get_engine():
    server = os.getenv("AZURE_SQL_SERVER")
    database = os.getenv("AZURE_SQL_DB")
    username = os.getenv("AZURE_SQL_USER")
    password = os.getenv("AZURE_SQL_PASSWORD")

    if not all([server, database, username, password]):
        raise ValueError("Faltan variables de entorno para la conexión.")

    connection_string = URL.create(
        "mssql+pyodbc",
        username=username,
        password=password,
        host=server,
        port=1433,
        database=database,
        query={"driver": "ODBC Driver 17 for SQL Server"},
    )

    return create_engine(connection_string)

def guardar_indicadores_pre(df: pd.DataFrame):
    engine = get_engine()
    try:
        df.to_sql("Indicadores_PRE_raw", con=engine, if_exists="append", index=False)
        print("✅ Datos insertados en Indicadores_PRE_raw.")
    except Exception as e:
        print("❌ Error al insertar en PRE:", str(e))
        raise

def guardar_indicadores_vpd(df: pd.DataFrame):
    engine = get_engine()
    try:
        df.to_sql("Indicadores_VPD_raw", con=engine, if_exists="append", index=False)
        print("✅ Datos insertados en Indicadores_VPD_raw.")
    except Exception as e:
        print("❌ Error al insertar en VPD:", str(e))
        raise
