'''
Author:     Maxwell Mougette
Contact:    mougette@wisc.edu
This project was made for the Zendesk Intern Coding Challenge.
'''

import requests
from flask import Flask, render_template, request, session


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "Max Is Awesome"


@app.route('/')
def home():
    ## Secure cookies to store repeatitly used vars
    session['pageNum'] = 1
    session['subdomain'] = 'mougette'
    session['user'] = 'mougette@wisc.edu'
    session['pswd'] = '***********' ## Temp password for GitHub
    session['url'] = 'https://' + session['subdomain'] + '.zendesk.com/api/v2/tickets.json?page[size]=25'

    ## Call the Zendesk API for tickets and count.json
    response = getResponse()
    jsonResponse = response.json()
    countResponse = getCountResponse()

    countJsonResponse = countResponse.json()
    statusCode = response.status_code
    tickets = jsonResponse['tickets']
    numTickets = countJsonResponse['count']['value']

    ## more sessions that can now be made after the response
    session['statusCode'] = response.status_code
    session['count'] = numTickets

    return render_template('page.html', statusCode = session['statusCode'], tickets = tickets,
                           numTickets = session['count'], pageNum = session['pageNum'])

@app.route('/<int:page_id>',  methods=['GET', 'POST'])
def pages(page_id):
    if request.method == 'POST':

        if (int(page_id) > session['pageNum']):
            response = getResponse()
            jsonResponse = response.json()
            i = 1
            while (i < int(page_id)):

                jsonResponse = getNextResponse(jsonResponse)
                statusCode = session['statusCode']
                i += 1

        else:
            response = getResponse()
            jsonResponse = response.json()
            i = 1
            while (i < int(page_id)):
                jsonResponse = getNextResponse(jsonResponse)
                statusCode = session['statusCode']
                i += 1

        session['pageNum'] = page_id
        tickets = jsonResponse['tickets']

        return render_template('page.html', statusCode=session['statusCode'], tickets=tickets,
                               numTickets=session['count'], pageNum=session['pageNum'])

    return "Whoopsie!! It looks like you might be lost!"

@app.route('/ticket/<int:ticket_id>',  methods=['GET', 'POST'])
def tickets(ticket_id):
    if request.method == 'POST':
        url = session['url']
        user = session['user']
        pswd = session['pswd']
        response = requests.get(url, auth=(user, pswd))
        jsonResponse = response.json()
        tickets = jsonResponse['tickets']
        for ticket in tickets:
            if (ticket['id'] == ticket_id):
                ## temp return -
                return render_template('ticket.html', ticket=ticket)

    return "Whoops! It looks like you might be lost!"

def getResponse():
    ## Set up the data needed for the Zendesk API request
    subdomain = session['subdomain']
    user = session['user']
    pswd = session['pswd']
    url = 'https://' + subdomain + '.zendesk.com/api/v2/tickets.json?page[size]=25'

    ## get the response from the Zendesk API
    response = requests.get(url, auth=(user, pswd))

    return response

def getCountResponse():
    ## Set up the data needed for the Zendesk API request
    subdomain = session['subdomain']
    user = session['user']
    pswd = session['pswd']
    countURL = 'https://' + subdomain + '.zendesk.com/api/v2/tickets/count.json'

    ## get the response from the Zendesk API
    countResponse = requests.get(countURL, auth=(user, pswd))

    return countResponse

def getNextResponse(jsonResponse):
    subdomain = session['subdomain']
    user = session['user']
    pswd = session['pswd']
    hasMore = jsonResponse['meta']['has_more']
    if (hasMore):
        nextUrl = jsonResponse['links']['next']
        session['url'] = nextUrl
        response = requests.get(nextUrl, auth=(user, pswd))
        nextJsonResponse = response.json()
        session['statusCode'] = response.status_code
        return nextJsonResponse
    return None

if __name__ == '__main__':
    app.run(host='localhost', port=3000)