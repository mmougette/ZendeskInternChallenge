# ZendeskInternChallenge
This project was made for the Zendesk Intern Coding Challenge using Flask and python3.
Author: Maxwell Mougette
Contact: mougette@wisc.edu

Notes for setup:
You will need to input the subdomain and base64 authentication in home() of server.py befoere api calls will work.
Additionally, you can change the port the flask app will run on at the very bottom of server.py
The venv folder was not uploaded to this repo, so you may need to pip install a few libraries to make sure requests and flask run on your device.

Note for tests:
Some of the tests in test.py were written as happy path tests with specific values in mind based off of my subdomain (mougette).
