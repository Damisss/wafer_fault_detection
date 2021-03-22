from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from kneed import KneeLocator
import matplotlib.pyplot as plt
import pandas as pd
import os
import logging

from wafer_fault_detection.utils.file_operation import save_model
from wafer_fault_detection.app_logger.logger import AppLogger

_logger = logging.getLogger(__name__)

class Cluster (BaseEstimator, TransformerMixin):

  def __init__(self, log_path:str, model_path:str, params:dict) -> None:
    self.log_path = log_path
    self.model_path = model_path
    self.params = params

  def fit (self, X:pd.DataFrame, y=None):
    try:
      #need fit method to accomodate the sklearn pipeline
      self.y = y
      return self
    except Exception as e:
      raise e

  def elbowFinder (self, data:pd.DataFrame) -> int:
    try:
      inertia = []
      for i in range(1, self.params['data_preprocessing']['KMeansClustering']['n_cluster_max']):
        kmean = KMeans(n_clusters=i, random_state=self.params['base']['random_state'])
        kmean.fit(data)
        inertia.append(kmean.inertia_)

      kn = KneeLocator(
        range(1, self.params['data_preprocessing']['KMeansClustering']['n_cluster_max']), 
        inertia, 
        curve=self.params['data_preprocessing']['KMeansClustering']['KneeLocator']['curve'], 
        direction=self.params['data_preprocessing']['KMeansClustering']['KneeLocator']['direction']
        )
      _logger.info(f'Optimal value for cluster is: {kn.knee}.')
     
      return kn.knee

    except Exception as e:
      _logger.info(f'Something went wrong while computing optimal cluster value: {e}.')
      raise e
  
  def transform (self, X:pd.DataFrame) -> pd.DataFrame:
    try:
      X = X.copy()
      # Normally we should scale the dataset. As it is just for prove of concept we will not scale the the dataset.
      # scaler = StandardScaler()
      # sacledData = scaler.fit_transform(X)
      
      numberOfCluster = self.elbowFinder(X)
      kmean = KMeans(n_clusters=numberOfCluster, random_state=self.params['base']['random_state'])
      pred = kmean.fit_predict(X)
      save_model(model=kmean, name='kmeans', path=self.model_path)
      X['clusters'] = pred
      X['labels'] = self.y
      
      f = open(os.path.join(self.log_path, 'data_clustering.txt'), 'a+')
      message = f'Data cluster are successfully done.\n'
      AppLogger.log(f, message)
      f.close()

      _logger.info(f'Data cluster are successfully done.')

      return X

    except Exception as e:
      f = open(os.path.join(self.log_path, 'data_clustering.txt'), 'a+')
      message = f'Something went wrong while performing data clustering {e}\n'
      AppLogger.log(f, message)
      f.close()
      _logger.info(f'Something went wrong while performing data clustering {e}\n')
      raise e