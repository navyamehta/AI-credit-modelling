from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

# Loading data

accepted_data_path = "final_data.csv"

accepted_data = pd.read_csv(accepted_data_path, engine="python")

final_X = accepted_data.drop("loan_status", axis = 1)
final_y = chosen_data.loan_status

os = SMOTE(random_state = 0)
X_train, X_test, y_train, y_test = train_test_split(final_X, final_y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X, os_data_y = os.fit_sample(X_train, y_train)
os_data_X = pd.DataFrame(data= os_data_X, columns= columns)
os_data_y= pd.DataFrame(data= os_data_y, columns= ['loan_status'])

logreg = LogisticRegression()
rfe = RFE(logreg, 10)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


valuable = [final_X.columns[i] for i in range(0, len(final_X.columns)) if rfe.ranking_[i] == 1]
print(valuable)

# chosen_data.to_csv("updated.csv")

