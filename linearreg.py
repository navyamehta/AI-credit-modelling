import pandas as pd
from sklearn.feature_selection import RFE
from sklearn import linear_model
import statsmodels.api as sm
import trainingdata

def getprediction(credutil, paymenthist, informalinc, histlength, debtincomeratio, emplength, phoneusage):
  temp = trainingdata.gettrainingdata()
  colling = ['id', 'credutil', 'paymenthist', 'informalinc', 'histlength', 'debtincomeratio', 'emplength', 'phoneusage']
  CreditData = pd.DataFrame(temp, columns = colling)
  X = CreditData[['credutil','paymenthist', 'informalinc', 'histlength', 'debtincomeratio', 'emplength', 'phoneusage']]
  Y = CreditData['id']
  regr = linear_model.LinearRegression()
  regr.fit(X, Y)
  print('Intercept: \n', regr.intercept_)
  print('Coefficients: \n', regr.coef_)
  credscore = regr.predict([[credutil, paymenthist, informalinc, histlength, debtincomeratio, emplength, phoneusage]])
  return credscore

