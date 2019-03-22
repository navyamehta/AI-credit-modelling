import pandas as pd
import trainingdata

temp = trainingdata.gettrainingdata()
colling = ['id', 'credutil', 'paymenthist', 'informalinc', 'histlength', 'debtincomeratio', 'emplength', 'phoneusage']
CreditData = pd.dataframe(temp, columns = colling)
print(CreditData)
