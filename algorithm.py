import xgboost
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# Loading data

def algorithm(loan_amnt, emp_length, home_ownership, annual_inc, verification_status, loan_status, title, delinq_2yrs,
             fico_range_low, fico_range_high, pub_rec, revol_bal, revol_util, tot_cur_bal, chargeoff_within_12_mths,
             public_rec_bankruptcies, total_il_high_credit_limit):
  
  clean_data_path = "clean_data.csv"
  clean_data = pd.read_csv(clean_data_path, engine="python")
  X = clean_data.drop(["loan_status", "int_rate"], axis = 1)
  
  hot_encoded_X = pd.get_dummies(X)
  y = clean_data.loan_status
  
  X_train = hot_encoded_X
  y_train = y
  
  model = XGBClassifier(n_estimators = 150, learning_rate = 0.05)
  model.fit(X_train, y_train)
  y_pred = model.predict(X_test)
  
  default_risk = model.predict_proba(hot_encoded_X)[:, 0] * 100
  clean_data['default_risk'] = default_risk
# chosen_data.to_csv("updated.csv")

