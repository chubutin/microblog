from flask import Flask, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)
lm = LoginManager(app)
db = SQLAlchemy(app)

from app import views, models