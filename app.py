import firebase_admin
from flask import Flask, render_template
from firebase_admin import credentials
from firebase_admin import db
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "FSDFJKDS"
cred = credentials.Certificate('./ServiceAccountKey.json')


firebase_admin.initialize_app(cred, {
  'databaseURL' : 'https://url-shotner-d5a21-default-rtdb.firebaseio.com',
  'databaseAuthVariableOverride': None
})

"""Form Class"""
class UrlForm(FlaskForm):
  longUrl = StringField('Long URL:', validators=[DataRequired()])
  converti = SubmitField('Convert')
  key = StringField('http://127.0.0.1:5000/')

def random_key():
  import random

# Random Password Generator

def passwGen():
    mainStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    n = 7
    key = ''

    for i in range(0, n + 1):
        t = random.randint(0,len(mainStr))
        
        key = key + mainStr[t]

    return key

@app.route('/',methods=('GET', 'POST'))
def appl():
  ref = db.reference('/')
  longurl = None
  form = UrlForm()
  key = None
  if form.validate_on_submit():
    longurl = form.longUrl.data
    print(form.key.data)
    if form.key.data == '':
      key = random_key()
      ref = db.reference('/')
      ref.child(key).set({
        'longUrl' : longurl,
        'key' : key
      })
    else:
      key = form.key.data
      ref.child(key).set({
        'longUrl' : longurl,
        'key' : key
      })
    form.longUrl.data=''
    form.key.data=''
  return render_template('app.html', form=form)