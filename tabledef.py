from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
	__tablename__ = "user_fin"
 
	id = Column(Integer, primary_key=True)
	username = Column(String)
	password = Column(String)
	name = Column(String)
	loan_amnt = Column(Float)
	emp_length = Column(Float)
	home_ownership = Column(Float)
	annual_inc = Column(Float)
	verification_status = Column(Float)
	title = Column(Float)
	delinq_2yrs = Column(Float)
	fico_range_low = Column(Float)
	fico_range_high = Column(Float)
	pub_rec = Column(Float)
	revol_bal = Column(Float)
	revol_util = Column(Float)
	tot_cur_bal = Column(Float)
	chargeoff_within_12_mths = Column(Float)
	public_rec_bankruptcies = Column(Float)
	total_il_high_credit_limit = Column(Float)
 
#----------------------------------------------------------------------
	def __init__(self, username, password, name, loan_amnt, emp_length, home_ownership, annual_inc, verification_status, title, delinq_2yrs, fico_range_low, 
		fico_range_high, pub_rec, revol_bal, revol_util, tot_cur_bal, chargeoff_within_12_mths, public_rec_bankruptcies, total_il_high_credit_limit):
		self.username = username
		self.password = password
		self.name = name 
		self.loan_amnt = loan_amnt 
		self.emp_length = emp_length
		self.home_ownership = home_ownership
		self.annual_inc = annual_inc
		self.verification_status = verification_status
		self.title = title
		self.delinq_2yrs = delinq_2yrs
		self.fico_range_low = fico_range_low
		self.fico_range_high = fico_range_high
		self.pub_rec = pub_rec
		self.revol_bal = revol_bal
		self.revol_util = revol_util
		self.tot_cur_bal = tot_cur_bal
		self.chargeoff_within_12_mths = chargeoff_within_12_mths
		self.public_rec_bankruptcies = public_rec_bankruptcies
		self.total_il_high_credit_limit = total_il_high_credit_limit
 
# create tables
Base.metadata.create_all(engine)