import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
 
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("admin","password","name1",344)
session.add(user)
 
user = User("python","python","name1",344)
session.add(user)
 
user = User("jumpiness","python","name1",222)
session.add(user)

# add more users...
 
# commit the record the database
session.commit()
 
session.commit()