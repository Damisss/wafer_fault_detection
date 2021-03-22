from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier


class DefaultModels ():
  def __init__(self):
    self.logisticRegression = LogisticRegression()
    self.svc = SVC()
    #self.kneighbors =  KNeighborsClassifier()
    self.randomForest = RandomForestClassifier(random_state=42)
    self.extraTrees = ExtraTreesClassifier(random_state=42)
    self.adaBoost = AdaBoostClassifier(random_state=42)
    self.gradientBoosting = GradientBoostingClassifier(random_state=42)
    self.xgboost = XGBClassifier(random_state=42)