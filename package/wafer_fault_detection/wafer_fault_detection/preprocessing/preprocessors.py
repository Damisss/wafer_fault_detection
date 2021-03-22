import os
from typing import NoReturn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import KNNImputer
import pandas as pd
import numpy as np
import logging 

_logger = logging.getLogger(__name__)

class RemoveColumns (BaseEstimator, TransformerMixin):

  def __init__(self, column_names:list) -> None:
    self.column_names = column_names

  def fit (self, X:pd.DataFrame, y=None):
    try:
      return self
    except Exception as e:
      _logger.info(f'Something went wrong while removing unwanted features: {e}')
      raise e
  
  def transform (self, X: pd.DataFrame) -> pd.DataFrame:
    try:
      columns = ','.join(self.column_names)
      X = X.copy()
      X = X.drop(self.column_names, axis=1)
  
      _logger.info(f'unwanted feature removed: {columns}')
      print(X.shape)
      return X
    except Exception as e:
      _logger.info(f'Something went wrong while removing unwanted features: {e}')
      raise e

class MissingValueInputer (BaseEstimator, TransformerMixin):
  
  def fit (self, X, y=None):
    try:
      X = X.copy()
      self.isNullPresent = False
      self.nanSum = X.isna().sum()
      for i in self.nanSum:
        if i > 0:
          self.isNullPresent = True
          _logger.info('Some columns have missing values.')
          break
      
      return self

    except Exception as e:
      _logger.info(f'Something went wrong while inputing missing value: {e}')
      raise e
  
  def transform (self, X: pd.DataFrame) -> pd.DataFrame:
    try:
      X = X.copy()
      if self.isNullPresent:
        inputer = KNNImputer(n_neighbors=3)
        inputedData = inputer.fit_transform(X)
        df = pd.DataFrame(inputedData, columns=X.columns)

        _logger.info('Missing values inputed')

        return df
      
      return X
    
    except Exception as e:
      _logger.info(f'Something went wrong while inputing missing value: {e}')
      raise e
