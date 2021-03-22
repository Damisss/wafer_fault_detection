import os
import shutil
import pandas as pd
import logging

from data_management import FileValidationDbOperation
from wafer_fault_detection.pipeline import pipeline
from wafer_fault_detection.utils import config
from wafer_fault_detection.utils.file_operation import  params_loader
from wafer_fault_detection.app_logger.logger import AppLogger

_logger = logging.getLogger(__name__)
_params = params_loader(path=os.path.join(config.PACKAGE_ROOT, 'utils/params.yaml'))
def training ():
  try:
    if os.path.isdir('wafer_fault_detection/models'):
      shutil.rmtree('wafer_fault_detection/models')
      os.makedirs('wafer_fault_detection/models')

      #Performed files validation and db operation as well
    _logger.info('Data validaion has started')

    filesValidation  = FileValidationDbOperation(
      _params['data_source']['batch_files'],
      _params['data_preparation']['validated_files_path'],
      _params['data_preparation']['good_data_path'],
      _params['data_preparation']['master_csv'],
      _params['data_preparation']['training_db']
      )

    filesValidation.start()
    _logger.info('Data validattion has successfully completed.')
    # Perform training and evaluation of the model
    df = pd.read_csv(_params['data_preparation']['master_csv'])
    pipeline(data=df)

    _logger.info('Models training has successfully completed.')

    f = open(os.path.join(config.APP_LOGS, 'training.txt'), 'a+')
    message = f'Models training has successfully completed.\n'
    AppLogger.log(f, message)

  except Exception as e:
    f = open(os.path.join(config.APP_LOGS, 'training.txt'), 'a+')
    message = f'Something went wrong while training.\n'
    AppLogger.log(f, message)
    raise e

if __name__ == '__main__':
  training()


