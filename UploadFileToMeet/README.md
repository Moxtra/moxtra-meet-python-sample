Python Sample Code for Moxtra APIs
================================

This repository contains Python sample code to launch a real-time meeting and 
upload the selected files to it using Moxtra SDKs and APIs.



Please feel free to clone the repository and follow the steps below.


## Setup

<<<<<<< HEAD
####Clone the sample project from github:
	git clone https://github.com/sanjayiyerkudaliprasannakumar/Pyhton-Sample-Code.git
=======
## Clone the sample project from github
	git clone https://github.com/Moxtra/xxxxxx

>>>>>>> origin/master

## Register your App
	You can register your Moxtra App here: https://developer.moxtra.com/nextapps. Once you register, 
	you will be provided with a unique client id and client secret key that is used to initialize 
	the Moxtra SDK.


## Authenticating your App
	You'll need your CLIENT_ID and CLIENT_SECRET to authenticate your app and get your access_token.

	Go to Python-Sample-Code/UploadFileToMeet/static.
	Open index.html and input your CLIENT_ID as shown below:
		
		var client_id = "INPUT YOUR CLIENT_ID"; 
		


	Go to Python-Sample-Code/UploadFileToMeet
	Open server.py and input your CLIENT_ID and CLIENT_SECRET as shown below:

		# Moxtra App Credentials from developer.moxtra.com
			client_id = "INPUT_YOUR_CLIENT_ID"
			client_secret = "INPUT_YOUR_CLIENT_SECRET"

## Set the path of the folder containing the files to be uploaded:
	You need to now set the path of the temp folder to your path as shown below:
		
		<input class="cbox" type="checkbox" align="middle" name="pic[]" value="/Users/sanjayiyer/Desktop/Python-Sample-Code/UploadFileToMeet/static/temp/sample.jpeg" id="file_path" />
		



## Running your App
	Now you're all set to run your App:

	Configure an application server for Python. In this example we have used Flask which is a light weight microframework for Python.
	Install Flask:

		pip install Flask
	

	Once you have it installed, run server.py using the following command:
			python server.py

	Once you run the above command, the url to run your app is displayed in the terminal.

	Usually your app should be accessible via: http://host:port/static/index.html

	For example the URL may look something like http://127.0.0.1:5000/static/index.html
 



## Step by Step tutorial


Here we are using a web page to drive server operations. The web page performs the following operations:

**1. Authenticate the user by generating the access token**

**2. Initialize the user**

**3. Start a Moxtra meet**

**4. Upload selected files to meet**

The upload file operations are to get files from server, not client. In other words, 
server codes are clients to Moxtra REST API Service. 

  + The Server operations are handled by Python-Sample-Code/UploadFileToMeet/server.py
 


## Step 1: Authenticate the user by generating the access token.
		The Core API uses Simple Single Sign On (SSO), but the Python SDK will take care 
		of most of it so you don't have to start from scratch. 

		You'll need to provide your CLIENT_ID inside the getToken function in index.html

				getToken = function()
	            {
	               	var uniqueid = "user001"; // You can replace this 
	               	with any Unique value of your own.
					var client_id = "INPUT YOUR CLIENT_ID HERE";


		You'll also need to provide your CLIENT_ID and CLIENT_SECRET inside server.py

		

			Sending the Request parameters to the get_access_token Python API:
			_________________________________________________________________
			Once the CLIENT_ID is input in the index.html, we will construct 
			the URL to fetch the data from the Python server:
				var req_url = "http://127.0.0.1:5000/getAccessToken?uniqueid=" + uniqueid;

			Now we will make an AJAX call to send this request to the Python API 
			on the App server to autenticate the user:
				jQuery.ajax({
	                    type: "GET",
	                    url: req_url,
	                    dataType: 'jsonp',
	                    cache: false,
	                    jsonpCallback: "getdata",
	                    success: function(response, status, xhr) {
	                        access_token = response.access_token;

	        This would return the access_token on successful authentication. 


## Step 2: Initilaize the user
        Using the access_token generated in the previous user, we initialize the user:

        	if (access_token) {
                        
                            var options = {
                                mode: "sandbox", 
                                client_id: client_id,
                                access_token: access_token,
                                invalid_token: function(event) {
                            // Triggered when the access token is expired or invalid
                                alert("Access Token expired for session id: " + event.session_id);
                                }
                            };

                            **Moxtra.init(options);** // Initialise the moxtra user

                        } 


## Step 3: Start a meet
		The user is authenticated and initialized onload of the webpage.
		Now the user clicks on the "Start Moxtra Meet", the start_meet() function gets invoked.
		In the start_meet() function, the meet_options variable is set with the required 
		parameters to start a moxtra meet.
		Now we make a call to Moxtra Javascript SDK to start a meet with the required parameters:
				Moxtra.meet(meet_options);

		On succesful start of the meet, the Javascript SDK returns the session_id and 
		the session_key of the meet.
		Any other user can be invited to join this meet using the session_key
		function start_meet() {
		                
		                var meet_options = {
		                    iframe: false, //To open the meet in the same window in a different iFrame.
		                    // tab: true, //To open the meet in a new browser tab, N/A if iframe option is set to true.
		                    tagid4iframe: "meet-container", //ID of the HTML tag within which the Meet window will show up. Refer https://developer.grouphour.com/moxo/docs-js-sdk/#meet
		                    iframewidth: "1000px",
		                    iframeheight: "750px",
		                    extension: { 
		                        "show_dialogs": { "meet_invite": true } 
		                    },
		                    start_meet: function(event) {
		                        console.log("Meet Started - session_id: "+event.session_id+"session_key: "+event.session_key);

		                        //Your application server can upload files to meet using the session_id and session_key
		                        var session_id=event.session_id;
		                        var session_key=event.session_key;
            
		                       uploadMeetFile(access_token,session_id,session_key);
		                    },
		                    error: function(event) {
		                        console.log("error code: " + event.error_code + " message: " + event.error_message);
		                    },
		                    end_meet: function(event) {
		                        console.log("Meet Ended");
		                    }
		                };
		                
		               **Moxtra.meet(meet_options);** //JS SDK call for Moxtra meet
		            }



## Step 4: Upload selected files to meet
		Once the moxtra meet is started, the user can access the session_id and session_key.
		Using this data, we now make a call to the the uploadMeetFile(access_token,session_id,session_key) in the index.html

		The selected file(s) data is captured and sent to the app server using the following url:
			var req_url = "http://127.0.0.1:5000/uploadFile?session_id=" + session_id + "&session_key=" + session_key + "&file_path=" + file_path;

		This in turn calls the upload_page() Python API method defined in server.py
					# Function to upload file
					@app.route('/uploadFile')
					def upload_page():
					    # TODO: please change the sessionid, key, name...
					    sessionid = request.args.get('session_id')
					    sessionkey = request.args.get('session_key')
					    filepath = request.args.get('file_path')

					    
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
					        print res.status_code
					        print res.text
					        response = make_response(res.text)
        

    				return response





For the detailed documentation on Moxtra APIs please visit [Moxtra Developer Website](http://developer.moxtra.com)






