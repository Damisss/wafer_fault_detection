import pandas as pd
import os
import logging

_logger = logging.getLogger(__name__)

class DataTransformation ():
  '''
    This class is used to transform the good data before loading it in Database
  '''
  @staticmethod
  def transformation (good_data_path:str)->None:
    try:
      #generate a list of good data paths
      files = [os.path.join(good_data_path, file) for file in os.listdir(good_data_path)]
      # loop over the list
      for file in files:
        df = pd.read_csv(file)
        # replace and nan value to NULL
        df.fillna('NULL', inplace=True)
        # replace values in Wafer column from wafer-123 to -123
        df['Wafer'] = df['Wafer'].str[6:]
        # save csv file
        df.to_csv(file, index=None, header=True)
      # log information 
      _logger.info('Data transformation completed.')
      

    except Exception as e:
      _logger.info('Something went wrong while performing data transformation.')
      raise e
