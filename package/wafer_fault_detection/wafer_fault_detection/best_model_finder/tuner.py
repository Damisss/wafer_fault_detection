import os
import itertools
import pickle
from sklearn.base import BaseEstimator
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
import logging

from wafer_fault_detection import __version__ as _version
from wafer_fault_detection.best_model_finder.default_models import DefaultModels
from wafer_fault_detection.best_model_finder.params import Params
from wafer_fault_detection.app_logger.logger import AppLogger
from wafer_fault_detection.utils import config
from wafer_fault_detection.utils.helper import  imbalance_hander
from wafer_fault_detection.utils.file_operation import load_model, save_model, params_loader

_logger = logging.getLogger(__name__)
_params =  params_loader(path=os.path.join(config.PACKAGE_ROOT, 'utils/params.yaml'))

class BestEstimatorFinder ():

  def best_estimator_for_svm (self, X, y=None):
    params = {
      'C':_params['training']['svc']['C'], 
      'gamma': _params['training']['svc']['gamma'],
      'kernel': _params['training']['svc']['kernel']
      }
    
    gs = GridSearchCV(SVC(), param_grid=params, cv=3, scoring='f1_macro')
    gs.fit(X, y)

    return gs.best_estimator_
  
    
  def best_estimator_for_logistic_regression (self, X, y=None):
    params = {
      'solver':_params['training']['logistic_regression']['solver'], 
      'penalty': _params['training']['logistic_regression']['penalty'],
      'C': _params['training']['logistic_regression']['C'],
      }
    
    gs = GridSearchCV(LogisticRegression(), param_grid=params, cv=3, scoring='f1_macro')
    gs.fit(X, y)

    return gs.best_estimator_
  
class BestModelFinder (BaseEstimator):
  def __init__(self, models_base_path= 'wafer_fault_detection/models'):
    #self.models = DefaultModels()
    self.params = Params()
    self.cv = KFold()
    self.models_base_path = models_base_path
  
  def fit(self, X, y=None):
    try:
      #self.estimators = dict()
      X = X.copy()
      clusterId = X['clusters'].unique()
      #instentaite best estimator finder class
      best_estimator_finder = BestEstimatorFinder()
      
      for i in clusterId:
        data = X[X['clusters'] == i]
        labels = data['labels']
        data = data.drop(['clusters', 'labels'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(
           data, 
           labels, 
           test_size=.2, 
           random_state=_params['base']['random_state']
           )

        X_train, y_train = imbalance_hander(X_train, y_train)
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        _logger.info(f'Parameters tuning of estimator for cluster {i} has strted.')
       # find best estimator using parameters tuning
        svc = best_estimator_finder.best_estimator_for_svm(X_train, y_train)
        svc_prediction = svc.predict(X_test)
        logistic_regression = best_estimator_finder.best_estimator_for_logistic_regression(X_train, y_train)
        logistic_regression_prediction = logistic_regression.predict(X_test)

        f1_score_for_svc = f1_score(y_test, svc_prediction)
        f1_score_for_logistic_regression = f1_score(y_test, logistic_regression_prediction)

        if f1_score_for_svc > f1_score_for_logistic_regression:
          save_model(model= svc, name='svc', path=f'wafer_fault_detection/models/svc_{i}')
        else:
          save_model(model= logistic_regression, name='logistic_regression', path=f'wafer_fault_detection/models/logistic_regression_{i}')
        
        _logger.info(f'Parameters tuning of estimator for cluster {i} has successfully completed.')

      f = open(os.path.join(config.APP_LOGS, 'parameters_tuning.txt'), 'a+')
      message = f'Parameters tuning has successfully completed.\n'
      AppLogger.log(f, message)
      f.close()
      _logger.info('Parameters tuning has successfully completed.')

      return self

    except Exception as e:
      f = open(os.path.join(config.APP_LOGS, 'parameters_tuning.txt'), 'a+')
      message = f'Something went wrong while performing model parameters tuning {e} \n'
      AppLogger.log(f, message)
      f.close()
      _logger.info(message)
      raise e
  
  def predict(self, X, y=None):
    try:
      X = X.copy()
      kmeans = load_model(path= os.path.join(config.KMEANS_PATH, f'Kmeans{_version}.pickle'))
      X = X.drop(['clusters', 'labels'], axis=1)
      clusters = kmeans.predict(X)
      X['clusters'] = clusters
      clusterId = X['clusters'].unique()

      _logger.info('Prediction has stated...')
      results = []
      for i in clusterId:
        data = X[X['clusters'] == i]
        data = data.drop(['clusters'], axis=1)
        scaler = StandardScaler()
        data = scaler.fit_transform(data)
        folder_name = [folder for folder in os.listdir(os.path.join(config.PACKAGE_ROOT, 'models')) if folder.endswith(f'_{i}')][0]
        folder_path = os.path.join(os.path.join(config.PACKAGE_ROOT, 'models'), folder_name)
        modelPath = os.path.join(folder_path, os.listdir(folder_path)[0])
        model = load_model(path= modelPath)
        preds = model.predict(data)

        for r in (preds):
          results.append(r)
      _logger.info('Prediction has been completed successfully.')
      return results

    except Exception as e:
      _logger.info('Something went wrong while performing prediction :{e}')
      raise e
