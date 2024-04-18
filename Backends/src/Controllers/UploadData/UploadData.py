from flask import Blueprint
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from Models.ConexionDB.dbConnection import get_db_connection # Conexion a la base de datos
from Models.Services.uploadServices import uploadServices
import os
import pandas as pd # type: ignore
from io import BytesIO
import numpy as np # type: ignore
from sklearn import tree # type: ignore
from sklearn.model_selection import cross_val_score # type: ignore
import matplotlib.pyplot as plt # type: ignore
from sklearn import tree # type: ignore
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score # type: ignore
import json


uploadData = Blueprint('upload',__name__)
ALLOWED_EXTENSIONS = {'xls', 'xlsx','csv'} #Extensiones permitidas en el upload del excel dt
UPLOAD_FOLDER = './src/Common/Files/' #Ruta del archivo temporal

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
@uploadData.route('/upload', methods=['POST']) # Metodo POST upload archivos 
def UploadDataToExcel():
    if 'file' not in request.files:
        return jsonify({'message':'No se subio ningun formato excel'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400
    if file and allowed_file(file.filename):
        try:
            excel_data = file.read()
            df = pd.read_excel(BytesIO(excel_data))
            #Calcular si el alumno aprueba la asignatura e insertar una columna con este valor en los datos, siendo 0 desaprobado y 1 aprobado , eliminamos las notas-1...
            df['state_note'] = df.apply(lambda row: 1 if (row["nota_1"] + row["nota_2"] + row["nota_3"] + row["nota_4"]) >= 40 else 0, axis=1)
            #df = df.drop(['nota-1', 'nota-2', 'nota-3','nota-4'], axis=1)
            #Eliminar Datos Nombre, Dni ,Apellidos, para el ingreso en la base de datos
            #print(df)
            df = df.drop(["Dni","Nombre","Ape. Paterno", "Ape. Materno"], axis=1)
            #Convertir los datos cualitativos en datos numéricos (0-1)
            df = pd.get_dummies(df,columns=["Zona", "Sexo", "Estado_Familia", "Trabajo_madre", 
                                            "Trabajo_padre","Apoderado","Estudio_extracurricular","Ayuda_familia", 
                                            "Tiene_internet","Actividad_Extracurricular"])
            #print(df.head())
            if len(df) > 0 :
                insert_dt = uploadServices.InsertDataFrameToDataBase(df) # insertar historical df
                insert_data_dt = uploadServices.InsertDataFrameToDataBase_DataTable(df) # insertar data_to_excel temporalmente
                if insert_dt and insert_data_dt:
                    #Datos Entrenamiento
                    df_historical = uploadServices.GetDataToDataBase_Historical_dt()
                    df_data_db_temp = uploadServices.GetDataToDataBase_Data_df()
                    df_historical = df_historical.drop(["nota_1","nota_2","nota_3", "nota_4"], axis=1)
                    df_data_db_temp = df_data_db_temp.drop(["nota_1","nota_2","nota_3", "nota_4"], axis=1)
                    
                    d_train = df_historical.iloc[:len(df_historical)//2]
                    d_test = df_historical.iloc[len(df_historical)//2:]
                    d_train_att = d_train.drop(['state_note'], axis=1) #Base de datos
                    print(f"variable : d_train_att {d_train_att}")
                    d_train_pass = d_train['state_note'] #Base de datos
                    d_test_att = d_test.drop(['state_note'], axis=1) #Base de datos
                    d_test_pass = d_test['state_note'] #Base de datos
                    d_att = df_data_db_temp.drop(['state_note'], axis=1) #Base de datos temporal
                    print(f"variable : d_att {d_att}")
                    d_pass = df_data_db_temp['state_note'] #Datos Excel
                    #Número de estudiantes que pasan en todo el dataset:
                    #print("Pasan: %d de %d (%.2f%%)" % (np.sum(d_pass), len(d_pass), 100*float(np.sum(d_pass)) / len(d_pass)))

                     # Ajustar a un árbol de decisión
                    t = tree.DecisionTreeClassifier(criterion="entropy", max_depth=5)
                    t = t.fit(d_train_att, d_train_pass) #jalor datos guardados de la base de datos clasificados por datos cualitativos
                    
                    # Calcular y mostrar el Accuracy así como mostrar la calificación promedio  +/- 2 desviaciones estandar (cubriendo el 95% de las calificaciones)
                    t.score(d_test_att, d_test_pass)
                    #print(t.score(d_test_att, d_test_pass))  
                    scores = cross_val_score(t, d_att, d_pass, cv=5)
                    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
                    
                    # Calcular y mostrar el Accuracy para profundidades del 1 al 19.
                    for max_depth in range(1, 20):
                        t = tree.DecisionTreeClassifier(criterion="entropy", max_depth=max_depth)
                        scores = cross_val_score(t, d_att, d_pass, cv=5)
                        #print("Max depth: %d, Accuracy: %0.2f (+/- %0.2f)" % (max_depth, scores.mean(), scores.std() * 2))
                        depth_acc = np.empty((19,3), float)
                        i = 0
                    for max_depth in range(1, 20):
                        t = tree.DecisionTreeClassifier(criterion="entropy", max_depth=max_depth)
                        scores = cross_val_score(t, d_att, d_pass, cv=5)
                        depth_acc[i,0] = max_depth
                        depth_acc[i,1] = scores.mean()
                        depth_acc[i,2] = scores.std() * 2
                        i += 1
                        depth_acc
                        
                    #Calcular y mostrar la matriz de confusión, con la máxima profundidad (2) que tiene el nivel de precisión mayor.
                    t = tree.DecisionTreeClassifier(criterion="entropy", max_depth=2)
                    t = t.fit(d_train_att, d_train_pass)
                    #t = t.fit(d_train_att, d_train_pass)

                    for indice, fila in d_att.iterrows():
                        fila_reshaped = fila.to_numpy().reshape(1, -1)              
                        y_pred = t.predict(fila_reshaped)
                    #cm = confusion_matrix(d_train_pass, y_pred) 
                    #posiciones = np.where(y_pred == 0)[0]
                    #print(f'Las posiciones donde y_pred es igual a 0 son: {posiciones}')
                    #cm_str = str(cm)
                    # Imprime la cadena de texto
                    #print(cm_str)
                    #estudiantes_jalados_df = df[df['state_note'] == 0]
                    #cantidad_estudiantes_jalados = len(estudiantes_jalados_df)
                    #indices_estudiantes_jalados = estudiantes_jalados_df.index.tolist()
                    #print("Cantidad de estudiantes que jalaron:", cantidad_estudiantes_jalados)
                    #print("Índices de estudiantes que jalaron:", indices_estudiantes_jalados)
                else:
                    return jsonify({
                            'success': False,
                            'message': 'datos no registrados en la base de datos.',
                        }),400
            return jsonify({
                        'success': True,
                        'message': 'Archivo cargado satisfactoriamente.'
                        #'data':json.dumps(cm.tolist())
                }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Formato de archivo no permitido'}), 400
