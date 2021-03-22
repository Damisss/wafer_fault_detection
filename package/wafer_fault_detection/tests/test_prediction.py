import pandas as pd
import os

from wafer_fault_detection.predict import make_prediction
from wafer_fault_detection.utils import config

def test_make_prediction ():
  test_data = pd.read_csv('wafer_fault_detection/pred_data/data.csv')

  subject = make_prediction(inputData=test_data)
  assert subject is not None
  assert subject[0] == 1