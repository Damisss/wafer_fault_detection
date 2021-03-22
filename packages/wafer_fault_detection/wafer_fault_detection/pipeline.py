import os
import logging 
from sklearn.pipeline import Pipeline
import pandas as pd

from wafer_fault_detection.preprocessing.clustering import Cluster
from wafer_fault_detection.preprocessing.preprocessors import RemoveColumns, MissingValueInputer
from wafer_fault_detection.best_model_finder.tuner import BestModelFinder
from wafer_fault_detection.app_logger.logger import AppLogger
from wafer_fault_detection.utils import config, file_operation

_logger = logging.getLogger(__name__)
_params = file_operation.params_loader(path=os.path.join(config.PACKAGE_ROOT, 'utils/params.yaml'))

def pipeline (*, data: pd.DataFrame) -> None:
  try:
    #intertia_cluster_path = os.path.join(config.PLOTS_PATH, 'intertia_clster.png')
    X = data.drop('Output', axis=1)
    y = data['Output']
    pipeline = Pipeline([
      ('inputer', MissingValueInputer()),
      ('remove', RemoveColumns(config.DROP_FEATURES)),
      ('clustering', Cluster(config.APP_LOGS, _params['data_preprocessing']['KMeansClustering']['model_path'], _params)),
      ('modelFinder', BestModelFinder())
    ])
    _logger.info('Pipeline fitted.')
    pipeline.fit(X, y)
    
    file_operation.save_model(model=pipeline, name='pipeline',path='wafer_fault_detection/models/pipeline')
    # writer log to a file
    f = open(os.path.join(config.APP_LOGS, 'pipeline.txt'), 'a+')
    message = 'Pipeline operation has successfully completed.'
    AppLogger.log(f, message)

    #show log in terminal
    _logger.info('Pipeline operation has successfully completed.')

  except Exception as e:
    f = open(os.path.join(config.APP_LOGS, 'pipeline.txt'), 'a+')
    message = f'Something went wrong while performing pipeline operation: {e} '
    AppLogger.log(f, message)
    raise e

