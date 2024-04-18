"""
Connects to a SQL database using pyodbc
"""
import pyodbc # type: ignore

# Parámetros de conexión
server = 'ALEXANDER'
database = 'AcademicMachineLearning'
username = 'sa'
password = '77657476'

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=yes;'

# Función para obtener la conexión
def get_db_connection():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print("Error de conexión:", e)
        return None