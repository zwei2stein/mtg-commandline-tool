from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

import io

import listTokens
import mtgCardTextFileDao

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/tokens')
def tokensPage():

	model = {}

	model["submitUrl"] = url_for('tokensProcess')

	return render_template('tokenForm.html', model=model)

@app.route('/listToken', methods=['POST'])
def tokensProcess():

	deckList = request.form['deckList']

	deck = mtgCardTextFileDao.readCardFile(io.StringIO(deckList), 'web', {}, True)

	response = listTokens.listTokens(deck)

	model = response

	model["submitUrl"] = url_for('tokensProcess')
	model["deckList"] = deckList

	return render_template('tokenForm.html', model=model)