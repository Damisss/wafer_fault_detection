from flask import Flask
from api.config import UPLOAD_FOLDER

def create_app(*, config_object) -> Flask:
  flask_app = Flask('ml_api')
  flask_app.config.from_object(config_object)
  flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  # import blueprints
  from api.controllers import prediction_app
  flask_app.register_blueprint(prediction_app)
  return flask_app 