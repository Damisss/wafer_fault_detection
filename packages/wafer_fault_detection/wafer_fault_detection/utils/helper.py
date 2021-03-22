from imblearn.combine import SMOTETomek
from imblearn.over_sampling import SMOTE


def imbalance_hander (XTrain, yTrain):
  try:
    smote = SMOTETomek(random_state=42, smote=SMOTE(k_neighbors=4))
    X_smt, y_smt = smote.fit_resample(XTrain, yTrain)
    return X_smt, y_smt
  except Exception as e:
    raise e

def featureNamesExtractor (acc, cur):
  try:
    if cur != 'Output':
       acc.append(acc.replace(' - ', '-'))
       return acc
    return acc
  except Exception as e:
    raise e
