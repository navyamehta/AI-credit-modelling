original_data_path = "accepted_2007_to_2018Q3.csv"

original_data = pd.read_csv(original_data_path, nrows=100000, engine="python")

features = ["loan_amnt", "int_rate", "emp_length", "home_ownership", "annual_inc",
           "verification_status", "loan_status", "title", "delinq_2yrs", "fico_range_low", "fico_range_high",
            "pub_rec", "revol_bal", "revol_util", "application_type", "tot_cur_bal", "chargeoff_within_12_mths", "pub_rec_bankruptcies",
           "total_il_high_credit_limit"]

# Features that are not numbers:
# One Hot encoding: home_ownership, verification_status, title ==== done
# Direct change:
# - emp_length: a years (2 <= a <= 10, 10+ years, <1 year)  ===== done
# - loan_status: only takes Charged Off and Fully Paid  ===== done
# - application_type: deals only with individual   ====== done

# Direct change first:

chosen_data = original_data[features]
chosen_data.drop(chosen_data[(chosen_data.loan_status != "Fully Paid") & (chosen_data.loan_status != "Charged Off")].index, inplace = True)

# Choose only individuals
chosen_data.drop(chosen_data[(chosen_data.application_type != "Individual")].index, inplace = True)
chosen_data = chosen_data.drop("application_type", axis = 1)

# Reformatting emp_length:
chosen_data["emp_length"].fillna(0, inplace = True)
emp_length_di = {"< 1 year": 0.5, "1 year": 1, "2 years": 2, "3 years": 3, "4 years": 4, "5 years": 5, "6 years": 6, "7 years": 7,
                "8 years": 8, "9 years": 9, "10+ years": 10}
chosen_data = chosen_data.replace({"emp_length": emp_length_di})

# Fill known empty columns
chosen_data['title'].fillna("Other", inplace = True)
util_median = chosen_data['revol_util'].median()
chosen_data['revol_util'].fillna(util_median, inplace = True)

# Double checking for empty cells
cols_with_missing = [col for col in chosen_data.columns if chosen_data[col].isnull().any()]
chosen_data = chosen_data.replace({"loan_status": {"Charged Off": 0, "Fully Paid": 1}})

chosen_data.to_csv("clean_data.csv")
