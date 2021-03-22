import os
UPLOAD_FOLDER = 'prediction_batch_files'
PREDICTION_VALIDATED_FILES_PATH = 'validated_files'
PREDICTION_GOOD_DATA_PATH = os.path.join(PREDICTION_VALIDATED_FILES_PATH, 'good_data')
PREDICTION_DB_PATH = 'services/prediction_wafer.db'
APP_LOGS = 'logs'
PREDICTION_RESULTS = 'prediction_results/results.csv'
FILE_FROM_DB = 'file_from_db/data.csv'


class Config ():
  TESTING = False
  DEBUG = False

class DevelopmentConfig (Config):
  DEVELOPMENT = True
  DEBUG = True

class TestConfig (Config):
  TESTING= True