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

@app.route('/authorize')
def authorize():
	auth_tokens = t.get_authentication_tokens(callback_url=request.url_root[:-1]+url_for('callback'))
	session['rts'] = auth_tokens
	return redirect(auth_tokens['auth_url'])
	
@app.route('/callback')
def callback():
	if not session.has_key('rts'):
		return 'Error: no request token stored in cookie.'
		
	rts = session['rts']
			
	if request.args.has_key('oauth_token') and request.args['oauth_token'] == rts['oauth_token']:
		if request.args.has_key('oauth_verifier'):
			tu = Twython(app_key=consumer_key, app_secret=consumer_secret,
		oauth_token=rts['oauth_token'], oauth_token_secret=rts['oauth_token_secret'])
			auth_tokens = tu.get_authorized_tokens(request.args['oauth_verifier'])

			save_token(auth_tokens, tokens)
			return redirect(url_for('thanks'))
	return 'Error: getting the incorrect access tokens.'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/thanks')
def thanks():
	return render_template('thanks.html')

@app.route('/tokens')
def show_tokens():
	return render_template('show_tokens.html', tokens=tokens)

@app.route('/tokens.csv')
def tokens_csv():
	fields = ['user_id', 'screen_name', 'oauth_token', 'oauth_token_secret']
	s = ','.join(fields) + '\n'
	for token in tokens:
		s += ','.join(map(lambda field: str(token[field]), fields)) + '\n'
	return Response(s, mimetype='application/csv')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=False, port=9001)