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

'''
    Default home page shows a list of the first 25 tickets
'''
@app.route('/')
def home():
    ## Sessions to store repeatitly used vars
    session['subdomain'] = 'mougette'  ## PLACE YOUR DOMAIN HERE
    session['basic'] = 'YOUR_BASE64_AUTH'  ## PLACE HOLDER FOR GITHUB
    session['pageNum'] = 1
    session['url'] = 'https://' + session['subdomain'] + '.zendesk.com/api/v2/tickets.json?page[size]=25'
    session['nextURL'] = ''
    session['prevURL'] = ''

    ## Call the Zendesk API for tickets (w/ 25 peer page)
    response = getResponse(session['url'])
    if (response == None):
        return "Whoops! It looks like someone's lost!"

    jsonResponse = response.json()
    tickets = jsonResponse['tickets']

    ## Call Zendesk API for count.json
    countResponse = getCountResponse()
    if (countResponse == None):
        return "Whoops! It looks like someone's lost!"

    countJsonResponse = countResponse.json()

    ## one more session that can now be made after the count response
    session['count'] = countJsonResponse['count']['value']

    return render_template('page.html', statusCode = session['statusCode'], tickets = tickets,
                           numTickets = session['count'], pageNum = session['pageNum'], hasMore = session['hasMore'])

'''
    Pages of additional pages of tickets upto 25 tickets per page
'''
@app.route('/<int:page_id>',  methods=['GET', 'POST'])
def pages(page_id):
    if request.method == 'POST':

        ## This is the case when advancing to the next page
        if (int(page_id) > session['pageNum']):
            response = getResponse(session['nextURL'])

        ## This is the case when going back to all tickets from individual ticket view
        elif(int(page_id) == session['pageNum']):
            response = getResponse(session['url'])

        ## This is the case when going back to the previous page
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

'''
    Page for full view of a single ticket
'''
@app.route('/ticket/<int:ticket_id>',  methods=['GET', 'POST'])
def tickets(ticket_id):
    if request.method == 'POST':
        response = requests.get(session['url'], headers={'Authorization': 'Basic ' + session['basic']})
        jsonResponse = response.json()
        tickets = jsonResponse['tickets']
        for ticket in tickets:
            if (ticket['id'] == ticket_id):
                return render_template('ticket.html', ticket=ticket, pageNum=session['pageNum'])

    return "Whoops! It looks like you might be lost!"

'''
    Accepts a url to the Zendesk API that specifies the specific page of tickets in the form:
    'https://' + session['subdomain'] + '.zendesk.com/api/v2/tickets.json?page[size]=25'
    
    Updates session info and returns the response if valid
    
    @Returns:
    -None if invalid url or invalid response
    -The response if the url and response are valid
'''
def getResponse(url):
    ## Check that the response is valid
    try:
        response = requests.get(url, headers={'Authorization': 'Basic ' + session['basic']})
        if (response.status_code != 200):
            return None
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

'''
    Gets and returns the count.json response from the Zendesk API
    This is used to get the total number of tickets
'''
def getCountResponse():
    ## Set up the data needed for the Zendesk API request
    countURL = 'https://' + session['subdomain'] + '.zendesk.com/api/v2/tickets/count.json'

    ## get the response from the Zendesk API
    try:
        ##response = requests.get(url, headers={'Authorization': 'Basic ' + session['basic']})
        countResponse = requests.get(countURL, headers={'Authorization': 'Basic ' + session['basic']})
        if (countResponse.status_code != 200):
            return None
    except requests.exceptions.MissingSchema:
        return None
    ## Make sure the response is a json
    try:
        jsonResponse = countResponse.json()
    except ValueError:
        # no JSON returned
        return None

    return countResponse

'''
    Note: If you have something running on port 3000, you can change it here
'''
if __name__ == '__main__':
    app.run(host='localhost', port=3000)