#!/usr/bin/python

from flask import Flask, Response, redirect, request, session, url_for, render_template
from twython import Twython
import random

from consumer_credentials import consumer_key, consumer_secret

t = Twython(app_key=consumer_key, app_secret=consumer_secret)

app = Flask(__name__)
# a secret key is needed to use session
app.secret_key = 'some secret'

tokens = []

def save_token(token, token_store):
	for x in token_store:
		if x['user_id'] == token['user_id']:
			x = token
			break
	else:
		token_store.append(token)

def check_and_set_session_id(fn):
	def wrapped(*args, **kwargs):
		if 'id' not in session:
			session['id'] = random.randint(0, 2**32)
		return fn(*args, **kwargs)
	return wrapped
	
@check_and_set_session_id
@app.route('/authorize')
def authorize():
	auth_tokens = t.get_authentication_tokens(callback_url=request.url_root[:-1]+url_for('callback'))
	session['rts'] = auth_tokens
	print 'Session ID %s: %s' % (session['id'], session['rts'])
	return redirect(auth_tokens['auth_url'])
	
@app.route('/callback')
def callback():
	print 'Session ID %s: %s' % (session['id'], request.args.items())
	
	if not session.has_key('rts'):
		return 'Error: no request token stored in cookie.'
		
	rts = session['rts']
			
	if request.args.has_key('oauth_token') and request.args['oauth_token'] == rts['oauth_token']:
		if request.args.has_key('oauth_verifier'):
			tu = Twython(app_key=consumer_key, app_secret=consumer_secret,
		oauth_token=rts['oauth_token'], oauth_token_secret=rts['oauth_token_secret'])
			auth_tokens = tu.get_authorized_tokens(request.args['oauth_verifier'])

			save_token(auth_tokens, tokens)
			print 'Session ID %s: %s' % (session['id'], auth_tokens)
			return 'authorization tokens: %s' % auth_tokens
	return 'Error: getting the incorrect access tokens.'

@check_and_set_session_id
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/tokens')
def show_tokens():
	return render_template('show_tokens.html', tokens=tokens)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=9001)