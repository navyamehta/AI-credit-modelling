from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from flask import Flask, render_template, flash, request, url_for, redirect, session
import ml

engine = create_engine('sqlite:///tutorial.db', echo=True)

app = Flask(__name__)
 
@app.route('/')
def man():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return redirect(url_for('home'))
 
@app.route('/login', methods=['POST'])
def do_admin_login():
 
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])
 	
	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	result = query.first()

	res = engine.execute('select * from user_fin where username = :1 and password = :2', [POST_USERNAME,POST_PASSWORD]).first()

	if result:
		session['logged_in'] = True
		session['id'] = res['id']
		return redirect(url_for('home'))
	else:
		flash('wrong password!')
		return home()

@app.route('/home')
def home():
	res = engine.execute('select * from user_fin where id = :1', [session['id']]).first()
	score = ml.mlalg(res['loan_amnt'],res['emp_length'],res['home_ownership'],res['annual_inc'],res['verification_status'],res['title'],res['delinq_2yrs']
		,res['fico_range_low'], res['fico_range_high'], res['pub_rec'], res['revol_bal'], res['revol_util'], res['tot_cur_bal'], res['chargeoff_within_12_mths'], res['public_rec_bankruptcies'],
		res['total_il_high_credit_limit'])
	return "Credit: " + str(score)

 
@app.route("/logout")
def logout():
	session['logged_in'] = False
	return home()
 
if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=4000)