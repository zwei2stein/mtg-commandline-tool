from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

import io

import listTokens
import deckPrice
import mtgCardTextFileDao

app = Flask(__name__)

def addSubmitUrlsToModel(model) :

	model["listTokensUrl"] = url_for('listTokensMethod')
	model["deckPriceUrl"] = url_for('deckPriceMethod')

	return model

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/tokens')
def tokensPage():

	model = {}

	model = addSubmitUrlsToModel(model)

	return render_template('tokenForm.html', model=model)

@app.route('/listTokens', methods=['POST'])
def listTokensMethod():

	deckList = request.form['deckList']

	deck = mtgCardTextFileDao.readCardFile(io.StringIO(deckList), 'web', {}, True)

	response = listTokens.listTokens(deck)

	model = response

	model = addSubmitUrlsToModel(model)

	model["deckList"] = deckList

	return render_template('tokenForm.html', model=model)

@app.route('/deckPrice', methods=['POST'])
def deckPriceMethod():

	deckList = request.form['deckList']

	deck = mtgCardTextFileDao.readCardFile(io.StringIO(deckList), 'web', {}, True)

	currency = 'eur'

	model = response = deckPrice.deckPrice(deck, currency)

	model = addSubmitUrlsToModel(model)

	model["deckList"] = deckList

	return render_template('tokenForm.html', model=model)