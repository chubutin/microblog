from flask import render_template, flash, redirect, url_for
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, current_user
from oauth import OAuthSignIn
from app import app, db, lm
from .forms import LoginForm
from models import User

# @app.route('/')
# @app.route('/index')
# def index():
# 	user = {'nickname': 'Chubutin'}  # fake user
# 	posts = [  # fake array of posts
# 	{ 
# 	'author': {'nickname': 'John'}, 
# 	'body': 'Beautiful day in Portland!' 
# 	},
# 	{ 
# 	'author': {'nickname': 'Susan'}, 
# 	'body': 'The Avengers movie was so cool!' 
# 	}
# 	]
# 	return render_template("index.html",
# 		title='Home',
# 		user=user,
# 		posts=posts)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="%s", remember_me=%s' %
#               (form.openid.data, str(form.remember_me.data)))
#         return redirect('/index')
#     return render_template('login.html', 
#                            title='Sign In',
#                            form=form,
#                            providers=app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
	print('entrando a index')
	return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    print("usuario no anonimo")
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    print('llamada despues de callback')
    print('social_id ' + social_id)
    print('username ' + username)
    print('email ' + email)
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
    	print('no existia el usuario, lo persisto')
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    print('usuario  no logueado')
    print(current_user.is_anonymous)
    print(current_user.is_authenticated)
    login_user(user, True)
    print('usuario logueado')
    print ('current user' + str(current_user))
    print str(user)
    return redirect(url_for('index'))