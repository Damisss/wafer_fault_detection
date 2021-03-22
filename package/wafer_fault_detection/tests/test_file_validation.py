import math
import pandas as pd
import pandas
import json
import os
import shutil
import pytest
import numpy as np


from wafer_fault_detection.raw_files_validation.validation import FileValidation
from wafer_fault_detection.predict import make_prediction
from wafer_fault_detection.utils import config
from wafer_fault_detection.utils import file_operation


regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
fileValidation = FileValidation(
'test_data', 
'test_logs'
)


@pytest.fixture
def foo():
  df = pd.DataFrame({'col1': [np.nan, np.nan, np.nan], 'col2': [9,2, 5], 'col3': [10, 4, 16]})
  df.to_csv(
  'test_data/wafer_13012020_090817.csv', 
  index=None, 
  header=True,
  encoding = "utf-8"
  )
  yield
  os.remove('test_data/wafer_13012020_090817.csv')
  

@pytest.fixture
def foo1():
  df = pd.DataFrame({'col1': [], 'col2': [], 'col3': []})
  df.to_csv(
  'test_data/Wafer_15010_130532.csv', 
  index=None, 
  header=True,
  encoding = "utf-8"
  )
  

@pytest.fixture
def foo3():
  df = pd.DataFrame({'col1': [np.nan, np.nan, np.nan], 'col2': [9,2, 5], 'col3': [10, 4, 16]})
  df.to_csv(
  'validatedFile/good_data/wafer_13012020_090817.csv', 
  index=None, 
  header=True,
  encoding = "utf-8"
  )
  

@pytest.mark.usefixtures('foo')
def test_valid_filename (mocker):
  spy1 = mocker.spy(fileValidation, 'file_name_validation')
  mocker.patch('shutil.copy2')

  fileValidation.file_name_validation(regex, 8, 6, 'validatedFile')
  spy1.assert_called_once_with(regex, 8, 6, 'validatedFile')
  shutil.copy2.assert_called_with(
    'test_data/wafer_13012020_090817.csv', 
    'validatedFile/good_data'
    )

@pytest.mark.usefixtures('foo1')    
def test_wrong_filename (mocker):
 
  spy1 = mocker.spy(fileValidation, 'file_name_validation')
  mocker.patch('shutil.copy2')

  fileValidation.file_name_validation(regex, 8, 6, 'validatedFile')
  spy1.assert_called_once_with(regex, 8, 6, 'validatedFile')
  shutil.copy2.assert_called_with(
    'test_data/Wafer_15010_130532.csv', 
    'validatedFile/bad_data'
    )
@pytest.mark.usefixtures('foo3')
def test_valid_column_numbers (mocker):
  spy1 = mocker.spy(fileValidation, 'columns_validation')
  mocker.patch('shutil.move')

  fileValidation.columns_validation(3, 'validatedFile','training')
  spy1.assert_called_once_with(3, 'validatedFile','training')
  shutil.move.assert_not_called()
 
@pytest.mark.usefixtures('foo3')
def test_wrong_column_numbers (mocker):
  
  spy1 = mocker.spy(fileValidation, 'columns_validation')
  mocker.patch('shutil.move')

  fileValidation.columns_validation(2, 'validatedFile', 'training')
  spy1.assert_called_once_with(2,'validatedFile', 'training')
  shutil.move.assert_called_with(
    'validatedFile/good_data/wafer_13012020_090817.csv', 
    'validatedFile/bad_data'
    )
@pytest.mark.usefixtures('foo3')
def test_empty_column (mocker):
  spy1 = mocker.spy(fileValidation, 'empty_column_validation')
  mocker.patch('shutil.move')

  fileValidation.empty_column_validation('validatedFile')
  spy1.assert_called_once_with('validatedFile')
  shutil.move.assert_called_with(
    'validatedFile/good_data/wafer_13012020_090817.csv', 
    'validatedFile/bad_data'
    )
  
  


