#!/usr/bin/python
# -*- coding: utf8 -*-

# Please install requests first if you don't have it: pip install requests
import requests
import hmac
import hashlib
import base64
import time
import re
import ntpath
from flask import request
from flask import make_response

from flask import Flask
app = Flask(__name__)
app.debug = True

# URL Endpoint to post the data
REQUEST_URL = "https://apisandbox.moxtra.com/oauth/token"

# URL Endpoint to post the data
UPLOAD_URL = "https://sandbox.moxtra.com/board/upload"

# Moxtra App Credentials from developer.moxtra.com
client_id = "INPUT_YOUR_CLIENT_ID"
client_secret = "INPUT_YOUR_CLIENT_SECRET"


# Function to upload file
@app.route('/uploadFile')
def upload_page():
    print "inside upload"
    # TODO: please change the sessionid, key, name...
    sessionid = request.args.get('session_id')
    sessionkey = request.args.get('session_key')
    filepath = request.args.get('file_path')

    #print filepath
    head, tail = ntpath.split(filepath)

    params = {
            "type": "original",
            "sessionid": sessionid,
            "key": sessionkey,
            "name": tail,
            }

    with open(filepath, 'rb') as f:
        print filepath
        data = f.read()
        res = requests.post(UPLOAD_URL, params = params, data = data)
        #print res.status_code
        #print res.text
        response = make_response(res.text)
        #print response

    return response


# Function to setup/initialize user and get access token
@app.route('/getAccessToken')
def get_access_token():

    #print client_id
    
    # Unique ID of how user is identified in your system
    unique_id = request.args.get('uniqueid')
    
    
    
    # User Information
    firstname = "John"
    lastname = "Doe"
    
    # Create signature
    timestamp = str(int(time.time() * 1000))
    #msg = client_id + unique_id + timestamp
    #signature = base64.urlsafe_b64encode(hmac.new(key=client_secret, msg=msg, digestmod=hashlib.sha256).digest())
    # remove the tail "="
    #signature = re.sub(r'=+$', '', signature)
    
    params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'http://www.moxtra.com/auth_uniqueid',
            'uniqueid': unique_id, 
            'timestamp': timestamp,
            'firstname': firstname,
            'lastname': lastname,
            }
    #r = request.post(REQUEST_URL, params = params)
    r = requests.post(REQUEST_URL, params = params)
    #print r.status_code
    #print r.text

    response = make_response(r.text)
    #print response

    return response


if __name__ == '__main__':
    app.run()

