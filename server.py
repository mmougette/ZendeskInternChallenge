'''
Author:     Maxwell Mougette
Contact:    mougette@wisc.edu
This project was made for the Zendesk Intern Coding Challenge.

TODO:
- Add more detailed error messages
- Add tests


'''

import requests
from flask import Flask, render_template, request, session


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "Max Is Awesome"


@app.route('/')
def home():
    ## Sessions to store repeatitly used vars
    session['pageNum'] = 1
    session['subdomain'] = 'mougette'
    session['basic'] = 'YOUR_BASE64_AUTH' ## PLACE HOLDER FOR GITHUB
    session['url'] = 'https://' + session['subdomain'] + '.zendesk.com/api/v2/tickets.json?page[size]=25'
    session['nextURL'] = ''
    session['prevURL'] = ''

    ## Call the Zendesk API for tickets and count.json
    response = getResponse(session['url'])
    jsonResponse = response.json()
    countResponse = getCountResponse()
    countJsonResponse = countResponse.json()
    statusCode = response.status_code
    tickets = jsonResponse['tickets']
    numTickets = countJsonResponse['count']['value']

    ## more sessions that can now be made after the response
    ##session['statusCode'] = response.status_code
    session['count'] = numTickets
    ##session['hasMore'] = jsonResponse['meta']['has_more']

    return render_template('page.html', statusCode = session['statusCode'], tickets = tickets,
                           numTickets = session['count'], pageNum = session['pageNum'], hasMore = session['hasMore'])

@app.route('/<int:page_id>',  methods=['GET', 'POST'])
def pages(page_id):
    if request.method == 'POST':

        if (int(page_id) > session['pageNum']):
            response = getResponse(session['nextURL'])

        elif(int(page_id) == session['pageNum']):
            response = getResponse(session['url'])

        else:
            response = getResponse(session['prevURL'])

        if (response == None):
            return "Whoops! It looks like someone's lost!"
        jsonResponse = response.json()
        session['pageNum'] = page_id
        tickets = jsonResponse['tickets']

        return render_template('page.html', statusCode=session['statusCode'], tickets=tickets,
                               numTickets=session['count'], pageNum=session['pageNum'], hasMore = session['hasMore'])

    return "Whoopsie!! It looks like you might be lost!"

@app.route('/ticket/<int:ticket_id>',  methods=['GET', 'POST'])
def tickets(ticket_id):
    if request.method == 'POST':
        url = session['url']
        user = session['user']
        pswd = session['pswd']
        response = requests.get(session['url'], headers={'Authorization': 'Basic ' + session['basic']})
        jsonResponse = response.json()
        tickets = jsonResponse['tickets']
        for ticket in tickets:
            if (ticket['id'] == ticket_id):
                ## temp return -
                return render_template('ticket.html', ticket=ticket, pageNum=session['pageNum'])

    return "Whoops! It looks like you might be lost!"

def getResponse(url):
    ## Check that the response is valid
    try:
        response = requests.get(url, headers={'Authorization': 'Basic ' + session['basic']})
    except requests.exceptions.MissingSchema:
        return None
    ## Make sure the response is a json
    try:
        jsonResponse = response.json()
    except ValueError:
        # no JSON returned
        return None

    ## Update sessions
    session['url'] = url
    session['nextURL'] = jsonResponse['links']['next']
    session['prevURL'] = jsonResponse['links']['prev']

    session['statusCode'] = response.status_code
    session['hasMore'] = jsonResponse['meta']['has_more']

    return response

def getCountResponse():
    ## Set up the data needed for the Zendesk API request
    countURL = 'https://' + session['subdomain'] + '.zendesk.com/api/v2/tickets/count.json'

    ## get the response from the Zendesk API
    countResponse = requests.get(countURL, headers={'Authorization': 'Basic ' + session['basic']})

    return countResponse


if __name__ == '__main__':
    app.run(host='localhost', port=3000)