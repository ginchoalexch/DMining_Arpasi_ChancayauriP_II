from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
import warnings
from Controllers.UploadData.UploadData import uploadData  
from config import config
from config_swagger import SwaggerConfig  

app = Flask(__name__)

@app.route('/')
def index():
    return 'Machine Learning - Prediccion de rendimiento academico'

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    app.config.from_object(config['development'])
    app.register_blueprint(SwaggerConfig.swagger_ui_blueprint, url_prefix=SwaggerConfig.SWAGGER_URL) 
    app.register_blueprint(uploadData, url_prefix='/api')
    app.run()
