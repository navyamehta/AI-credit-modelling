import xgboost
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# Loading data

['Unnamed: 0', 'loan_amnt', 'emp_length', 'annual_inc', 'delinq_2yrs',
       'fico_range_low', 'fico_range_high', 'pub_rec', 'revol_bal',
       'revol_util', 'tot_cur_bal', 'chargeoff_within_12_mths',
       'pub_rec_bankruptcies', 'total_il_high_credit_limit',
       'home_ownership_ANY', 'home_ownership_MORTGAGE', 'home_ownership_OWN',
       'home_ownership_RENT', 'verification_status_Not Verified',
       'verification_status_Source Verified', 'verification_status_Verified',
       'title_Business', 'title_Car financing',
       'title_Credit card refinancing', 'title_Debt consolidation',
       'title_Green loan', 'title_Home buying', 'title_Home improvement',
       'title_Major purchase', 'title_Medical expenses',
       'title_Moving and relocation', 'title_Other', 'title_Vacation']

def makearray(loan_amnt, emp_length, home_ownership, annual_inc, verification_status, loan_status, title, delinq_2yrs,
             fico_range_low, fico_range_high, pub_rec, revol_bal, revol_util, tot_cur_bal, chargeoff_within_12_mths,
             public_rec_bankruptcies, total_il_high_credit_limit):
       home_ownership_ANY = 0;
       home_ownership_MORTGAGE = 0;
       home_ownership_OWN = 0;
       home_ownership_RENT = 0;
       verification_status_NotV = 0;
       verification_status_SV = 0;
       verification_status_V = 0;
       title_Business = 0;
       title_Car = 0;
       title_cc = 0;
       title_Debt = 0;
       title_green = 0;
       title_homeb = 0;
       title_homei = 0;
       title_major = 0;
       title_medical = 0;
       title_moving = 0;
       title_other = 0;
       title_vacation = 0;
       if (home_ownership == "ANY"):
              home_ownership_ANY = 1
       if (home_ownership == "MORTGAGE"):
              home_ownership_MORTGAGE = 1
       if (home_ownership == "OWN"):
              home_ownership_OWN = 1
       if (home_ownership == "RENT"):
              home_ownership_RENT = 1
       if (verification_status == "NOT VERIFIED"):
              verification_status_NotV = 1
       if (verification_status == "SOURCE VERIFIED"):
              verification_status_SV = 1
       if (verification_status == "VERIFIED"):
              verification_status_V = 1
       if (title == "BUSINESS"):
              title_Business = 1
       if (title == "CAR FINANCING"):
              title_Car = 1
       if (title == "CREDIT CARD FINANCING"):
              title_cc = 1
       if (title == "DEBT CONSOLIDATION"):
              title_Debt = 1
       if (title == "GREEN LOAN"):
              title_green = 1
       if (title == "HOME BUYING"):
              title_homeb = 1
       if (title == "HOME IMPROVEMENT"):
              title_homei = 1
       if (title == "MAJOR PURCHASE"):
              title_major = 1
       if (title == "MEDICAL EXPENSES"):
              title_medical = 1
       if (title == "MOVING AND RELOCATION"):
              title_moving = 1
       if (title == "OTHER"):
              title_other = 1
       if (title == "VACATION"):
              title_vacation = 1
       return [loan_amnt, emp_length, annual_inc, delinq_2yrs, fico_range_low, fico_range_high, pub_rec, revol_bal, revol_util, 
               tot_cur_bal, chargeoff_within_12_mths, pub_rec_bankruptcies, total_il_high_credit_limit, home_ownership_ANY, 
               home_ownership_MORTGAGE, home_ownership_OWN, home_ownership_RENT, verification_status_NotV,
               verification_status_SV, verification_status_V, title_Business, title_Car, title_cc, title_Debt, title_green,
               title_homeb, title_homei, title_major, title_medical, title_moving, title_other, title_vacation]


def mlalg(loan_amnt, emp_length, home_ownership, annual_inc, verification_status, loan_status, title, delinq_2yrs,
             fico_range_low, fico_range_high, pub_rec, revol_bal, revol_util, tot_cur_bal, chargeoff_within_12_mths,
             public_rec_bankruptcies, total_il_high_credit_limit):
       dataarr = makearray(loan_amnt, emp_length, home_ownership, annual_inc, verification_status, loan_status, title, delinq_2yrs,
                           fico_range_low, fico_range_high, pub_rec, revol_bal, revol_util, tot_cur_bal, chargeoff_within_12_mths,
                           public_rec_bankruptcies, total_il_high_credit_limit)
       clean_data_path = "clean_data.csv"
       clean_data = pd.read_csv(clean_data_path, engine="python")
       X = clean_data.drop(["loan_status", "int_rate"], axis = 1)
       hot_encoded_X = pd.get_dummies(X)
       y = clean_data.loan_status
       X_train = hot_encoded_X
       y_train = y
       model = XGBClassifier(n_estimators = 150, learning_rate = 0.05)
       model.fit(X_train, y_train)
       X_test = pd.DataFrame(datarr, columns = 
       y_pred = model.predict(X_test)
       default_risk = model.predict_proba(hot_encoded_X)[:, 0] * 100
  clean_data['default_risk'] = default_risk
# chosen_data.to_csv("updated.csv")



