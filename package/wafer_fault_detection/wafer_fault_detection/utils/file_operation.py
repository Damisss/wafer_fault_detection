import pickle
import os
import shutil
import json
import typing as tp
from datetime import datetime
import yaml
import logging

from wafer_fault_detection import __version__ as _version

_logger = logging.getLogger(__name__)

def save_model (*, model, name:str, path:str)-> None:
  try:
    # delete folder if it exist otherwise create it
    if os.path.isdir(path):
      shutil.rmtree(path)
      os.makedirs(path)
    else:
      os.makedirs(path)
    #serialize the model
    saved_file_name = os.path.join(path, f'{name}{_version}.pickle')
    with open(saved_file_name, 'wb') as f:
      f.write(pickle.dumps(model))
    _logger.info(f'save model: {saved_file_name}')
  
  except Exception as e:
    raise e

def load_model (*, path:str)-> None:
  try:
    with open(path, 'rb') as f:
      model = pickle.loads(f.read())

    _logger.info(f'model loaded: {path}')
    return model
  except Exception as e:
    raise e

def grab_schema_values (*, schema_path:str) -> tp.Tuple[str, int, int, int, dict]:
  try:
    with open(schema_path, 'r') as f:
        # load schema json file
      data = json.load(f)
    #grab different variable (file name, length of date stamp and length of time stamp, number of columns and columns)
    sampleFileName = data['SampleFileName']
    lengthOfDateStampInFile = data['LengthOfDateStampInFile']
    lengthOfTimeStampInFile = data['LengthOfTimeStampInFile']
    numberofColumns = data['NumberofColumns']
    colName = data['ColName']

    return sampleFileName, lengthOfDateStampInFile, lengthOfTimeStampInFile, numberofColumns, colName

  except Exception as e:
    raise e

def regex () -> str:
    try:
       #regex based on the "FileName" given in "Schema" file.
       #it is used to validate training batch filename.
      return  "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
    except Exception as e:
      raise e

def make_folder(*, path: str) -> None:
  try:

    if not os.path.isdir(path):
      os.makedirs(path)
  
  except OSError:
    raise OSError

def delete_folder (*, path:str) -> None:
  try:

    if os.path.isdir(path):
      shutil.rmtree(path)

  except OSError:
    raise OSError

def move_file_to_archive (*, base_path:str)->None:
  try:
    
    now = datetime.now()
    date = now.date()
    time = now.strftime('%H%M%S')
    # generate a list of bad files
    #basePath = os.path.join(self.validatedFile,'bad_data')
    bad_data_files = [os.path.join(base_path, f) for f in os.listdir(base_path)]
    
    if os.path.isdir(base_path):

      dest = f'archive_bad_data/bad_data_{str(date)}_{str(time)}'
      #create archive dir if it doesn't exist yet
      if not os.path.isdir(dest):
        os.makedirs(dest)

      # move file to archive
      for file in bad_data_files:
          if file not in os.listdir(dest):
            shutil.move(file, dest)
      # write information to log
      
      #delete bad data folder
      if os.path.isdir(base_path):
        shutil.rmtree(base_path)

  except Exception as e:
    raise e


def params_loader (*, path:str)->dict:
  with open(path, 'r') as f:
    params =  yaml.safe_load(f)
    return params