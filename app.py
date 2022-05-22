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

@app.errorhandler(404)
def invalid_route(e):
  return {'error':{
    'message' : 'Invalid Route'
  }}

"""App Route"""
@app.route('/app',methods=('GET', 'POST'))
def application():#App Route Handler
  sp = None
  ref = db.reference('/')
  longurl = None
  form = UrlForm()
  key = None
  smallurl = None
  if form.validate_on_submit():
    sp = ref.order_by_key().get()
    """Automatic Key Generation"""
    if form.key.data == '':
      key = random_key()

      """Checking Key Is Already Used"""
      if key in sp.keys():
        smallurl = 'Alias Name Used'
        return render_template('app.html', form=form, shorturl=smallurl)
      else:
        longurl = form.longUrl.data
        ref.child(key).set({
          'longUrl' : longurl,
          'key' : key
        })

    else:
      key = form.key.data

      """Checking Key Is Already Used"""
      if key in sp.keys():
        smallurl = 'Alias Name Used'
        return render_template('app.html', form=form, shorturl=smallurl)

      else:
        longurl = form.longUrl.data 
        ref.child(key).set({
          'longUrl' : longurl,
          'key' : key
        })

    form.longUrl.data=''
    smallurl = 'https://shortit1.herokuapp.com/' + key
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