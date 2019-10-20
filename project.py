from flask import Flask, render_template, request, redirect,url_for, abort, flash, jsonify, session
import DataModels
import APIManager
import json


app = Flask(__name__)

@app.route('/')
@app.route('/captcha/')
def captcha():
	images = []
	message = ""
	success = True
	return render_template("front.html", images = images, message = message, success = success)

@app.route('/captcha/images/', methods = ['GET'])
def getImages():
	prev_images = []
	if 'captcha-prev-images' in session:
		prev_images = session['captcha-prev-images'].split('|')

	images = APIManager.getCaptchaImages(6,prev_images)
	cur_images = ''
	for i in images:
		if cur_images == '':
			cur_images = i.url
		else:
			cur_images += '|'+i.url
	session['captcha-prev-images'] = cur_images
	print cur_images
	resp = DataModels.AppResponse(True, 'OK','OK')
	resp.data =[i.serialize() for i in images]
	return jsonify(resp.serialize())

@app.route('/captcha/validate/', methods = ['POST'])
def validate():
	images = request.get_json()
	resp = APIManager.validteCaptchaSelection(images)
	return jsonify(resp.serialize())
	
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)