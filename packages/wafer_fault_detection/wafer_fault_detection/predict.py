import os
from wafer_fault_detection.utils.file_operation import load_model
from wafer_fault_detection.utils import config
from wafer_fault_detection import __version__ as _version

def make_prediction (*,inputData) -> list:
  try:
    pipeline = load_model(path=os.path.join(config.PACKAGE_ROOT, f'models/pipeline/pipeline{_version}.pickle'))
    prediction = pipeline.predict(inputData)
    return prediction

  except Exception as e:
    raise e