import os
import shutil
import re
import pandas as pd
import logging

from wafer_fault_detection.utils import file_operation
from wafer_fault_detection.app_logger.logger import AppLogger

_logger = logging.getLogger(__name__)

class FileValidation ():
  '''
  This class is used to perform training files validations
  '''

  def __init__(self, batch_files_path, log_path):
    self.batch_files_path =  batch_files_path
    self.log_path = log_path
  
  def file_name_validation (self, regex, lengthOfDateStampInFile, lengthOfTimeStampInFile, validated_files_path):
    try:
      good_dir = os.path.join(validated_files_path, 'good_data')
      bad_dir = os.path.join(validated_files_path, 'bad_data')
      #delete both existing good and bad data dir and then create new one.
      file_operation.delete_folder(path=good_dir)
      file_operation.delete_folder(path=bad_dir)
      file_operation.make_folder(path=good_dir)
      file_operation.make_folder(path=bad_dir)

      f = open(os.path.join(self.log_path, 'file_validation_log.txt'), 'a+')
      # loop over training batch files
      for file in os.listdir(self.batch_files_path):
        # perform first validation using regex
        if re.match(regex, file):
          split_in_dot = file.split('.')[0].split('_')
          date_stamp_length = len(split_in_dot[1])
          time_stamp_length = len(split_in_dot[2])
          # copy file to good data folder if length of date stamp and length of time stamp
          # are equal to those defined in schema json file otherwise copy it to bad folder
          if date_stamp_length == lengthOfDateStampInFile and time_stamp_length == lengthOfTimeStampInFile:
            shutil.copy2(os.path.join(self.batch_files_path, file), good_dir)
            message = f'file moved to good data folder: {file} \n'
            AppLogger.log(f, message)
          else:
            shutil.copy2(os.path.join(self.batch_files_path, file), bad_dir)
            message = f'file moved to bad data folder: {file} \n'
            AppLogger.log(f, message)
        
        else:
          # copy file to bad data folder
          shutil.copy2(os.path.join(self.batch_files_path, file), bad_dir)
          message = f'file moved to bad data folder: {file} \n'
          AppLogger.log(f, message)
  
      f.close()
      _logger.info('File name validation completed')

    except Exception as e:
      file = open(os.path.join(self.log_path, 'file_validation_log.txt'), 'a+')
      message = f'Something went wrong while validatng file name {e} \n'
      AppLogger.log(file, message)
      file.close()
      _logger.info(message)
      raise e
    
  
  def columns_validation (self, number_of_columns, validated_files_path, task):
    try:
      good_dir = os.path.join(validated_files_path, 'good_data')
      bad_dir = os.path.join(validated_files_path, 'bad_data')
      # grab list of good file data
      files = [os.path.join(good_dir, file) for file in os.listdir(good_dir)]
      f = open(os.path.join(self.log_path, 'file_validation_log.txt'), 'a+')
      #loop over good files and then do nothing if number of columns is equal to the one 
      #indicated in json file otherwise move file to bad data folder
      col_num = number_of_columns if task == 'training' else number_of_columns - 1
     
      for file in files:
        df = pd.read_csv(file)
        if df.shape[1] == col_num:
          continue
        shutil.move(file, bad_dir)
        message = f'file moved to bad data folder: {file} \n'
        AppLogger.log(f, message)

      f.close()
      _logger.info('Columns validation completed')

    except Exception as e:
      file = open(os.path.join(self.log_path, 'file_validation_log.txt'), 'a+')
      message = f'Something went wrong while moving file to bad data {e} \n'
      AppLogger.log(file, message)
      file.close()
      _logger.info(message)
      raise e

  
  def empty_column_validation (self, validated_files_path):
    try:
      good_dir = os.path.join(validated_files_path, 'good_data')
      bad_dir = os.path.join(validated_files_path, 'bad_data')
      # grab list of good file data
      files = [os.path.join(good_dir, file) for file in os.listdir(good_dir)]
      #log file object
      f = open(os.path.join(self.log_path, 'file_validation_log.txt'), 'a+')
      #loop over good files and then move file to bad folder if there is at least an empty columns
      for file in files:
        df = pd.read_csv(file)
        count= 0

        for name in df.columns:
          if (len(df[name]) - df[name].count()) == len(df[name]):
            count += 1
            shutil.move(file, bad_dir)
            message = f'file moved to bad data folder: {file} \n'
            AppLogger.log(f, message)
            break

        if count == 0:
          df.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
          df.to_csv(file, index=None, header=True)

      f.close()
      _logger.info('empty columns validation completed.')

    except Exception as e:
      file = open(os.path.join(self.log_path, 'file_validation_log.txt'), 'a+')
      message = f'Something went wrong while validating empty columns {e} \n'
      AppLogger.log(file, message)
      file.close()
      _logger.info(message)
      raise e