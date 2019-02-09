import azure.cognitiveservices.speech as speechsdk
import time

speech_key = "6fd6a1d3a05742f8bfaf9ffdccfffbb6"
service_region = "westus"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Set up the speech recognizer
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

done = False

def stop_cb(evt):
    """callback that stops continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    speech_recognizer.stop_continuous_recognition()
    done = True

# Connect callbacks to the events fired by the speech recognizer
rec = ""

speech_recognizer.recognizing.connect(lambda evt: print(evt.result.text))
speech_recognizer.recognized.connect(lambda evt: print("REC: " + rec.join(evt.result.text)))
speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
# stop continuous recognition on either session stopped or canceled events
speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)


# Start continuous speech recognition
speech_recognizer.start_continuous_recognition()
while not done:
    time.sleep(.5)
