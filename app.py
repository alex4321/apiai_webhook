#!/usr/bin/env python

from urllib.parse import urlencode
from urllib.request import urlopen
import json
import os
from flask import Flask, request, make_response
from apiai_webhook import WebHookAnswer
from apiai_webhook import WebHookRequest
app = Flask(__name__)


# noinspection PyPackageRequirements
@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook")
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = process_request(WebHookRequest(req)).as_dict
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def process_request(req):
    if req.result.action != "yahooWeatherForecast":
        return WebHookAnswer()
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = make_yql_query(req)
    if yql_query is None:
        return WebHookAnswer()
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = make_webhook_result(data)
    return res


def make_yql_query(req):
    city = req.result.parameters.get("geo-city")
    if city is None:
        return None
    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def make_webhook_result(data):
    query = data.get('query')
    if query is None:
        return {}
    result = query.get('results')
    if result is None:
        return {}
    channel = result.get('channel')
    if channel is None:
        return {}
    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}
    condition = item.get('condition')
    if condition is None:
        return {}
    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')
    print("Response:")
    print(speech)
    return WebHookAnswer(
        speech=speech,
        display_text=speech,
        source="apiai-weather-webhook-sample"
    )


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port {0}".format(port))
    app.run(debug=False, port=port, host='0.0.0.0')