import firebase_admin
from flask import Flask
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('./securitykey.json')

firebase_admin.initialize_app(cred, {
  'databaseURL' : 'https://url-shotner-d5a21-default-rtdb.firebaseio.com',
  'databaseAuthVariableOverride':'url'
})
