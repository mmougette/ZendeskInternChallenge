'''
Author:     Maxwell Mougette
Contact:    mougette@wisc.edu
This project was made for the Zendesk Intern Coding Challenge.
'''

from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    ## Set up the data needed for the Zendesk API request
    subdomain = 'mougette'
    user = 'mougette@wisc.edu'
    pswd = '***********' ## place holder password for github haha
    url = 'https://' + subdomain + '.zendesk.com/api/v2/tickets.json?page[size]=25'

    ## get the response from the Zendesk API
    response = requests.get(url, auth=(user, pswd))

    ## vars to be passed into the render template
    jsonResponse = response.json()
    statusCode = response.status_code
    tickets = jsonResponse['tickets']


    return render_template('page.html', statusCode = statusCode, tickets = tickets)

@app.route('/<page_id>')
def pages(page_id):
    return 'This is page ' + str(page_id)


if __name__ == '__main__':
    app.run(host='localhost', port=3000)