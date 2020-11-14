import unittest
from server import *

## Happy path testing!
class MyTestCase(unittest.TestCase):

    """
        Test getResponse(url) with a valid url
        This tests assumes session fields for url, subdomain, and basic are valid in server.py
        Given valid url, response should be non None
    """
    def test_getResponse_valid(self):
        with app.test_client() as client:
            client.get('/')
            ## Easy one just to test default session data loaded
            self.assertEqual(session['pageNum'], 1, 'Page Num Session Test')

            response = getResponse(session['url'])
            self.assertNotEqual(response, None, 'getResponse Valid URL Test')

    """
        Test getResponse(url) with an invalid url
        Given an invalid url, response should be None
    """
    def test_getResponse_invalid(self):
        with app.test_client() as client:
            client.get('/')
            response = getResponse('abcdefg')
            self.assertEqual(response, None, 'getResponse Invalid URL Test')

    """
        Happy path test for getResponse(url) with a valid url.
        This tests that the response is the expected json file
        with expected status code, number of tickets, and has more tickets
    """
    def test_getResponse_json(self):
        with app.test_client() as client:
            client.get('/')
            response = getResponse(session['url'])
            jsonResponse = response.json()
            statusCode = response.status_code
            hasMore = jsonResponse['meta']['has_more']
            tickets = jsonResponse['tickets']

            self.assertEqual(statusCode, 200, 'Test Status Code')
            self.assertEqual(hasMore, True, 'Test Has More')
            self.assertEqual(len(tickets), 25, 'Test Number of Tickets')

    """
        Happy path test for getCountResponse()
        Test that getCountResponse returns a json with the correct ['count']['value']
        Using my subdomain (mougette) I know there are 102 tickets
    """
    def test_getCountResponse(self):
        with app.test_client() as client:
            client.get('/')
            countResponse = getCountResponse()
            countJsonResponse = countResponse.json()
            count = countJsonResponse['count']['value']
            self.assertEqual(count, 102, 'Testing getCountResponse')


if __name__ == '__main__':
    unittest.main()
