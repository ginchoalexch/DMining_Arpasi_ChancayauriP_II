from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from config import config
from config_swagger import SwaggerConfig  

app = Flask(__name__)

@app.route('/')
def index():
    return 'CAMBIO RAMA ALEXANDER CH'

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_blueprint(SwaggerConfig.swagger_ui_blueprint, url_prefix=SwaggerConfig.SWAGGER_URL) 
    app.run()
