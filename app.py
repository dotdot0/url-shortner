import firebase_admin
from flask import Flask, redirect, render_template
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
  'databaseAuthVariableOverride': {'uid': 'user'}
})

"""Form Class"""
class UrlForm(FlaskForm):
  longUrl = StringField('Long URL:', validators=[DataRequired()])
  converti = SubmitField('Convert')
  key = StringField('https://shortit1.herokuapp.com/')

def random_key():
    mainStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    n = 7
    key = ''

    for i in range(0, n + 1):
        t = random.randint(0,len(mainStr))
        
        key = key + mainStr[t]

    return key
    

@app.route("/")
def hello_world():
    return redirect("/app")

@app.route('/app',methods=('GET', 'POST'))
def application():
  ref = db.reference('/')
  longurl = None
  form = UrlForm()
  key = None
  smallurl = None
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
    smallurl = 'https://shortit1.herokuapp.com/' + form.key.data
  return render_template('app.html', form=form, shorturl=smallurl)

@app.route('/hello')
def hello():
  return render_template('home.html')

@app.route('/<key>')
def mainRedirect(key):
  ref = db.reference('/')
  snapshot = ref.order_by_key().get()
  lurl = snapshot[key]['longUrl']
  return redirect(lurl)