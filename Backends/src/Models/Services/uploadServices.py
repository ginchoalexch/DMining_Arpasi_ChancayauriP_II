from Models.ConexionDB.dbConnection import get_db_connection
from flask import Flask, request, jsonify
import pandas as pd # type: ignore


class uploadServices:
    
    #Insertar Datos Excel a la tabla historical_dt para futuros entrenamientos.
    def InsertDataFrameToDataBase(dataFrame):
        conn = get_db_connection()
        if conn:
            try:
                query = f'INSERT INTO Historical_df (Zona,Tamanio_Familia,Sexo,Estado_Familia,Trabajo_madre,Trabajo_padre,Apoderado,Tiempo_viaje,Tiempo_estudio,Nro_cursos_desaprobados,Estudio_extracurricular,Ayuda_familia,Actividad_Extracurricular,Tiene_internet,Nro_inasistencias,nota_1,nota_2,nota_3,nota_4,state_note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                #for valor in dataFrame['Tamanio_Familia']: Inserta 1 valor en la base de datos
                #    conn.execute(query,valor) # inserta un valor en la base de datos
                for index, row in dataFrame.iterrows():
                    conn.execute(query, row["Zona_C"], row['Tamanio_Familia'], row['Sexo_M'], row['Estado_Familia_C'],row['Trabajo_madre_S'], 
                                 row['Trabajo_padre_S'], row['Apoderado_S'], row['Tiempo_viaje_escuela'], row['Tiempo_estudio'], row['Nro_cursos_desaprobados'],
                                 row['Estudio_extracurricular_S'], row['Ayuda_familia_S'], row['Actividad_Extracurricular_S'], row['Tiene_internet_S'],
                                 row['Nro_inasistencias'], row['nota_1'], row['nota_2'], row['nota_3'], row['nota_4'], row['state_note'])
                    conn.commit()
                conn.close()
                return True
            except Exception as e:
                return e
        else:
            return False
        
    #Obtener datos de entrenamientos registrados anteriormente en el Historical_dt
    def GetDataToDataBase_Historical_dt():
        conn = get_db_connection()
        if conn:
            try:
                query = f'SELECT * FROM Historical_df'
                df = pd.read_sql_query(query,conn)
                conn.close()
                return df
            except Exception as e:
                return e
        else:
            return False
     #Obtener datos de entrenamientos registrados anteriormente en el Historical_dt
    def GetDataToDataBase_Data_df():
        conn = get_db_connection()
        if conn:
            try:
                query = f'SELECT * FROM Data_df'
                df = pd.read_sql_query(query,conn)
                conn.close()
                return df
            except Exception as e:
                return e
        else:
            return False
        
    #Insertar Datos Excel a la tabla historical_dt para futuros entrenamientos.
    def InsertDataFrameToDataBase_DataTable(dataFrame):
        conn = get_db_connection()
        if conn:
            try:
                query_delete = f'DELETE FROM Data_df'
                conn.execute(query_delete) #Eliminamos los datos temporales
                query = f'INSERT INTO Data_df (Zona,Tamanio_Familia,Sexo,Estado_Familia,Trabajo_madre,Trabajo_padre,Apoderado,Tiempo_viaje,Tiempo_estudio,Nro_cursos_desaprobados,Estudio_extracurricular,Ayuda_familia,Actividad_Extracurricular,Tiene_internet,Nro_inasistencias,nota_1,nota_2,nota_3,nota_4,state_note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                #for valor in dataFrame['Tamanio_Familia']: Inserta 1 valor en la base de datos
                #    conn.execute(query,valor) # inserta un valor en la base de datos
                for index, row in dataFrame.iterrows():
                    conn.execute(query, row["Zona_C"], row['Tamanio_Familia'], row['Sexo_M'], row['Estado_Familia_C'],row['Trabajo_madre_S'], 
                                 row['Trabajo_padre_S'], row['Apoderado_S'], row['Tiempo_viaje_escuela'], row['Tiempo_estudio'], row['Nro_cursos_desaprobados'],
                                 row['Estudio_extracurricular_S'], row['Ayuda_familia_S'], row['Actividad_Extracurricular_S'], row['Tiene_internet_S'],
                                 row['Nro_inasistencias'], row['nota_1'], row['nota_2'], row['nota_3'], row['nota_4'], row['state_note'])
                    conn.commit()
                conn.close()
                return True
            except Exception as e:
                return e
        else:
            return False