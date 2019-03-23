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
	if session.get('logged_in'):
		return redirect(url_for('home'))
	else:
		return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
 
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])
 	
	Session = sessionmaker(bind=engine)
	s = Session()

	res = engine.execute('select * from user_final where username = :1 and password = :2', [POST_USERNAME,POST_PASSWORD]).first()

	if res != None:
		session['logged_in'] = True
		session['id'] = res['id']
		return redirect(url_for('home'))
	else:
		flash('wrong password!')
		return redirect(url_for('login_page'))

@app.route('/home')
def home():
	if not session.get('logged_in'):
		return redirect('/')
	else:
		res = engine.execute('select * from user_final where id = :1', [session['id']]).first()

		if res['loan_amnt'] == None:
			return redirect(url_for('calc_page'))
		else:
			score = ml.mlalg(res['loan_amnt'],res['emp_length'],res['home_ownership'],res['annual_inc'],res['verification_status'],res['title'],res['delinq_2yrs']
			,res['fico_range_low'], res['fico_range_high'], res['pub_rec'], res['revol_bal'], res['revol_util'], res['tot_cur_bal'], res['chargeoff_within_12_mths'], res['public_rec_bankruptcies'],
			res['total_il_high_credit_limit'])
			print(score)
			print(res['home_ownership'])
			print(res['title'])

			return  render_template('dashboard-formsubmit.html', score=int(score), name=res['username'])

 
@app.route("/logout")
def logout():
	session['logged_in'] = False
	return redirect('/')


@app.route('/calc',  methods=['POST'])
def calc():
	if not session.get('logged_in'):
		return redirect('/')

	loan_amnt = str(request.form['loan_amnt'])
	emp_length = str(request.form['emp_length'])
	home_ownership = str(request.form['home_ownership'])
	annual_inc = str(request.form['annual_inc'])
	verification_status = "NOT VERIFIED"
	title = str(request.form['title'])
	delinq_2yrs = 0
	fico_range_low = 690
	fico_range_high = 690
	pub_rec = 0
	revol_bal = 10000
	revol_util = 30
	tot_cur_bal = 10000
	chargeoff_within_12_mths = 0
	public_rec_bankruptcies = 0
	total_il_high_credit_limit = 0

	engine.execute('update user_final set loan_amnt = :1, emp_length = :2, home_ownership  = :3, annual_inc  = :4, verification_status  = :5, title  = :6, delinq_2yrs  = :7, fico_range_low  = :8, fico_range_high  = :9, pub_rec  = :10, revol_bal  = :11, revol_util = :12, tot_cur_bal = :13, chargeoff_within_12_mths = :14, public_rec_bankruptcies = :15, total_il_high_credit_limit = :16 where id = :17'
		, [loan_amnt,emp_length, home_ownership, annual_inc, verification_status, title, delinq_2yrs, fico_range_low, fico_range_high,
		pub_rec, revol_bal, revol_util, tot_cur_bal, chargeoff_within_12_mths, public_rec_bankruptcies, total_il_high_credit_limit, session['id']])

	return redirect(url_for('home'))


@app.route('/update',  methods=['POST'])
def update():
	if not session.get('logged_in'):
		return redirect('/')

	loan_amnt = str(request.form['loan_amnt'])
	emp_length = str(request.form['emp_length'])
	home_ownership = str(request.form['home_ownership'])
	annual_inc = str(request.form['annual_inc'])
	title = str(request.form['title'])

	print(loan_amnt)


	if(loan_amnt != ''):
		engine.execute('update user_final set loan_amnt = :1 where id = :2', [loan_amnt,session['id']])
	if(emp_length != ''):
		engine.execute('update user_final set emp_length = :1 where id = :2', [emp_length,session['id']])
	if(annual_inc != ''):
		engine.execute('update user_final set annual_inc = :1 where id = :2', [annual_inc,session['id']])

	engine.execute('update user_final set home_ownership = :1 where id = :2', [home_ownership,session['id']])
	engine.execute('update user_final set title = :1 where id = :2', [title,session['id']])

	return redirect(url_for('home'))
 
@app.route('/calc_page')
def calc_page():
	if not session.get('logged_in'):
		return redirect('/')
	res = engine.execute('select * from user_final where id = :1', [session['id']]).first()
	return render_template('dashboard-in.html',name=res['username'])

@app.route('/signup')
def signup():
	return render_template('register.html')

@app.route('/go_update')
def go_update():
	if not session.get('logged_in'):
		return redirect('/')
	res = engine.execute('select * from user_final where id = :1', [session['id']]).first()
	return render_template('update.html',name=res['username'], loan_amnt=res['loan_amnt'], emp_length=res['emp_length'], home_ownership=res['home_ownership'], annual_inc=res['annual_inc'], title=res['title'])

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/legal')
def legal():
	return render_template('legal.html')

@app.route('/login_page')
def login_page():
	if session.get('logged_in'):
		return redirect(url_for('home'))
	return render_template('login.html')


@app.route('/make_signup' , methods=['POST'])
def make_signup():
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])
 	
	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	result = query.first()

	if result: 
		flash("User already registered!")
		return redirect(url_for('signup'))
	else:
		engine.execute('insert into user_final (username,password) values (:1,:2)', [POST_USERNAME,POST_PASSWORD])
		return redirect(url_for('login_page'))

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=4000)