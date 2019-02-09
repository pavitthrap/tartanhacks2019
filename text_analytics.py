#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from pprint import pprint

subscription_key = "cc5ab8a32df6484981ec582e6669bd36"
assert subscription_key

text_analytics_base_url = "https://eastus2.api.cognitive.microsoft.com/text/analytics/v2.0"

key_phrase_api_url = text_analytics_base_url + "/keyPhrases"
print(key_phrase_api_url)

text1 = "Hello John Doe, Your payment for your Airbnb is due this Monday. Please respond to this email with your credit card information. Or give us a phone call at this number 1(800)-666-0000 to make your payment. Make sure to respond by this Monday, else your account will be subject to 10% interest per day. Airbnb Team"

documents = {'documents' : [
  {'id': '1', 'language': 'en', 'text': text1},
]}

headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
key_phrases = response.json()

from IPython.display import HTML
table = []
for document in key_phrases["documents"]:
    text    = next(iter(filter(lambda d: d["id"] == document["id"], documents["documents"])))["text"]
    phrases = ",".join(document["keyPhrases"])
    print(text, phrases)


pprint(key_phrases)
