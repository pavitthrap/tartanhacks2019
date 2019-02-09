import os 

from flask import Flask, g, render_template, request, url_for
import json 
import threading
#from . import db

def after_this_request(f):
	print("after called")
	if not hasattr(g, 'after_request_callbacks'):
		g.after_request_callbacks = []
	g.after_request_callbacks.append(f)
	return f

###############################
import azure.cognitiveservices.speech as speechsdk
import time
import requests
from pprint import pprint
import re

counter = 0

subscription_key = "cc5ab8a32df6484981ec582e6669bd36"
assert subscription_key

text_analytics_base_url = "https://eastus2.api.cognitive.microsoft.com/text/analytics/v2.0"


speech_key = "6fd6a1d3a05742f8bfaf9ffdccfffbb6"
service_region = "westus"
key_phrase_api_url = text_analytics_base_url + "/keyPhrases"
senti_phrase_api_url = text_analytics_base_url + "/sentiment"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Set up the speech recognizer
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

done = False


#################

demo = False
curr_text = ""

speech_recognizer.recognizing.connect(lambda evt: curr_text.join(evt.result.text))
speech_recognizer.recognized.connect(lambda evt: analyze_speech(rec.join(evt.result.text)))
speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
# stop continuous recognition on either session stopped or canceled events

#################################################

def sustain_speech():
    print("sustain called")
    speech_recognizer.start_continuous_recognition()
    for i in range(15):
        time.sleep(.5)
    print("CURR TEXT IS", curr_text)
    speech_recognizer.stop_continuous_recognition()

def stop_cb(evt):
    #"""callback that stops continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    speech_recognizer.stop_continuous_recognition()
    done = True

 ################################################

speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)









def create_app(test_config=None):
	# create and configure the app 
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev', 
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)

	if test_config is None:
		#load the instance config, if it exists, when not testing 
		app.config.from_pyfile('config.py', silent=True)
	else:
		#load the test config if passed in 
		app.config.from_mapping(test_config)


	#ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

    # a simple page that says hello 
	@app.route('/hello')
	def hello():
		return 'Hello, World!'

	#@app.before_request	
	@app.route('/', methods=('GET', 'POST'))
	def index(screen_text="Unknown Caller!"):
	    # row = get_db().execute(
	    #         'SELECT * FROM status WHERE id = (SELECT MAX(id) FROM status);'
	    #     ).fetchone()
	    
	    """Show all the posts, most recent first."""
	    print("show index")
	    global demo
	    state = getattr(g, 'state', None)
	    if state is None:
	        g.state = 1


	    if request.method == 'POST':
	        #print(dir(request))
	        
	        request_JSON = request.data
	        print(request_JSON)
	        #request_JSON = json.dumps(request_JSON)
	        request_JSON = request_JSON.decode('utf-8')
	        print(request_JSON)
	        if 'phonedemo' in request.form:
	        	print("1")
	        	g.state = 1
	        elif 'appdemo' in request.form:
	        	print("2")
	        	g.state = 4
	        elif 'name=startdemo' == request_JSON:
	        	print("STARTTTT")
	        	demo=True
	        	print("demo is NOW", demo)
	        elif 'name=getupdate' == request_JSON: 
	        	#print("GET UPDATE")
	        	screen_text = curr_text

	        print("going to return")
	        return render_template('blog/index.html', screen_text=curr_text)

	    # db = get_db()
	    # posts = db.execute(
	    #     'SELECT p.id, title, body, created, author_id, username'
	    #     ' FROM post p JOIN user u ON p.author_id = u.id'
	    #     ' ORDER BY created DESC'
	    # ).fetchall()
	    return render_template('blog/index.html')

	from flaskr import db
	db.init_app(app)

	from flaskr import auth
	app.register_blueprint(auth.bp)

	from flaskr import blog
	app.register_blueprint(blog.bp)
	app.add_url_rule('/', endpoint='index')

	@app.before_first_request
	def activate_job():
	    def run_demo():
	        global demo
	        while not demo:
	        	time.sleep(1)
	        	pass
	        print("demo is gn start")
	        sustain_speech()

	    thread = threading.Thread(target=run_demo)
	    thread.start()

	return app