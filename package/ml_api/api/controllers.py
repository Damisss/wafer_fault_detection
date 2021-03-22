from flask import Blueprint, request, jsonify, Response
import os
import shutil
import pandas as pd
#from werkzeug.utils import secure_file

from api.helper import allowed_file
from api import config
from wafer_fault_detection.predict import make_prediction
from wafer_fault_detection import __version__ as _version
from wafer_fault_detection.data_management import FileValidationDbOperation
#from wafer_fault_detection.models import pipeline


prediction_app = Blueprint('prediction_app', __name__)

@prediction_app.route('/health', methods=['GET'])
def health ():
  if request.method == 'GET':
    return 'ok'

@prediction_app.route('/v1/predict', methods=['POST'])
def prediction ():
  if request.method == 'POST':

    if 'files' not in request.files:
      return Response('No file found')
    if os.path.isdir(config.UPLOAD_FOLDER):
      shutil.rmtree(config.UPLOAD_FOLDER)
      os.makedirs(config.UPLOAD_FOLDER)
    else:
      os.makedirs(config.UPLOAD_FOLDER)

    files = request.files.getlist('files')

    for file in files:

      if file and allowed_file(file=file.filename):
        #filename = secure_filename(file.filename)
        file.save(os.path.join(config.UPLOAD_FOLDER, file.filename))
        
    fileValidation = FileValidationDbOperation(
      config.UPLOAD_FOLDER, 
      config.PREDICTION_VALIDATED_FILES_PATH,
      config.PREDICTION_GOOD_DATA_PATH,
      config.FILE_FROM_DB,
      config.PREDICTION_DB_PATH,
      sqlPath = 'services/prediction.sql',
      task = 'prediction',
      logFolderPath= config.APP_LOGS,
      schema='schema.json'
    )
    fileValidation.start()
    data = pd.read_csv(config.FILE_FROM_DB)
    results = make_prediction(inputData=data)
    df = pd.DataFrame(results, columns=['Prediction'])
    df.to_csv(config.PREDICTION_RESULTS, index=None, header=True)

    return Response("Prediction has been completed successfully!")
