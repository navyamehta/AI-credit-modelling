import xgboost as xgboost
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

from xgboost import XGBRegressor
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression


# Loading data

accepted_data_path = "accepted_2007_to_2018Q3.csv"

accepted_data = pd.read_csv(accepted_data_path, nrows=20000, engine="python")

features = ["loan_amnt", "int_rate", "emp_length", "home_ownership", "annual_inc",
           "verification_status", "loan_status", "title", "delinq_2yrs", "fico_range_low", "fico_range_high", "mths_since_last_delinq", "mths_since_last_record",
            "pub_rec", "revol_bal", "revol_util", "application_type", "tot_cur_bal", "chargeoff_within_12_mths", "pub_rec_bankruptcies",
           "total_il_high_credit_limit"]

# Features that are not numbers:
# One Hot encoding: home_ownership, verification_status, title,  
# Direct change:
# - emp_length: a years (2 <= a <= 10, 10+ years, <1 year)  ===== done
# - loan_status: only takes Charged Off and Fully Paid  ===== done
# - application_type: deals only with individual   ====== done

# Direct change first:

chosen_data = accepted_data[features]
chosen_data.drop(chosen_data[(chosen_data.loan_status != "Fully Paid") & (chosen_data.loan_status != "Charged Off")].index, inplace = True)
chosen_data.drop(chosen_data[(chosen_data.application_type != "Individual")].index, inplace = True)

chosen_data = chosen_data.drop("application_type", axis = 1)


chosen_data["emp_length"].fillna(0, inplace = True)
emp_length_di = {"< 1 year": 0.5, "1 year": 1, "2 years": 2, "3 years": 3, "4 years": 4, "5 years": 5, "6 years": 6, "7 years": 7,
                "8 years": 8, "9 years": 9, "10+ years": 10}
chosen_data = chosen_data.replace({"emp_length": emp_length_di})

# One hot encoding:

X = chosen_data.loc[:, chosen_data.columns != 'loan_status']
y = chosen_data.loc[:, chosen_data.columns == 'loan_status']

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y = os.fit_sample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['loan_status'])

logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# X = chosen_data.drop("loan_status", axis = 1)


# final_y = chosen_data.loan_status

# final_X = pd.get_dummies(X)
# chosen_data.to_csv("updated.csv")
