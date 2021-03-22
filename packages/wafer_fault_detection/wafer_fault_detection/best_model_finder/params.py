class Params ():
  def __init__(self):
    self.svcParams = {
      'C':range(1, 10), 
      'gamma': [0.001, 0.005, 0.1, 0.5],
      'kernel': ['linear', 'poly', 'rbf']
      }
    self.xgboostParams =  {
      'max_depth': [3, 4, 5, 6, 7, 8, 10],
      'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3, 0.4],
      'colsample_bytree': [0.6, 0.8, 1, 2, 3],
      'colsample_bylevel': [0.6, 0.8, 1, 2, 3],
      'gamma': [0.6, 0.8, 1, 2],
      'min_split_loss': [0.0, 0.01, 0.1],
      'reg_lambda': range(2, 10, 2),
      'n_estimators': [100, 150, 200, 250],
      }
    self.gradientBoostingParams = {
      'n_estimators': [100, 150, 200, 250],
      'learning_rate':[0.01, 0.05, 0.1, 0.2, 0.3], 
      'loss': ['deviance', 'exponential'],
      'criterion': ['friedman_mse', 'mse', 'mae'],
      'max_features':['auto', 'sqrt', 'log2'],
      }

    self.adaboostParams = {
      'n_estimators': [100, 150, 200, 250, 300], 
      'learning_rate':[0.01, 0.05, 0.1, 0.2, 1., 2., 10.], 
      'algorithm':['SAMME', 'SAMME.R']
      }
    
    self.randomForestParams = {
      'n_estimators':[150, 300, 600], 
      'min_samples_leaf':[2, 3],  
      'min_samples_split':[14, 12], 
      'max_features':[0.7, 1],
      'criterion': ['gini', 'entropy']
      }
    
    self.extratreesParams = {
      'n_estimators': [100, 150, 200, 250], 
      'criterion': ['gini', 'entropy'],
      'max_depth': range(2, 9), 
      'max_features': ['auto','sqrt', 'log2']
      }
    
    # self.kneighborsParams = {
    #   'weights':['uniform', 'distance'],
    #   'algorithm':['auto', 'ball_tree', 'kd_tree', 'brute'],
    #   'leaf_size': range(5, 40, 3),
    #   'metric':['minkowski', 'precomputed'],
    #   'n_neighbors':range(2, 15, 1),
    #   'p': [2, 3, 5]
    #   }
    self.logisticRegressionParams = {
      'solver': ['newton-cg', 'lbfgs', 'liblinear'],
      'penalty': ['l2'],
      'C': [100, 10, 1.0, 0.1, 0.01]
    }