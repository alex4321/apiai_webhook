#!/usr/bin/env python

from urllib.parse import urlencode
from urllib.request import urlopen
import json
import os
from apiai_webhook import Application, WebHookAnswer, WebHookRequest

def process_request(req):
    print("ACTION : ", req.result.action)
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = make_yql_query(req)
    if yql_query is None:
        return WebHookAnswer()
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    print("Query URL : " + yql_url)
    result = urlopen(yql_url).read().decode('utf8')
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
    print("QUERY : ", json.dumps(query))
    if query is None:
        return WebHookAnswer()
    result = query.get('results')
    print("RESULTS : ", json.dumps(result))
    if result is None:
        return WebHookAnswer()
    channel = result.get('channel')
    print("CHANNEL : ", json.dumps(channel))
    if channel is None:
        return WebHookAnswer()
    item = channel.get('item')
    print("ITEM : ", json.dumps(item))
    location = channel.get('location')
    print("LOCATION : ", json.dumps(location))
    units = channel.get('units')
    print("UNITS : ", json.dumps(units))
    if (location is None) or (item is None) or (units is None):
        return {}
    condition = item.get('condition')
    print("CONDITION : ", json.dumps(condition))
    if condition is None:
        return {}
    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')
    print("SPEECH : ", json.dumps(speech))
    print("Response:")
    print(speech)
    return WebHookAnswer(
        speech=speech,
        display_text=speech,
        source="apiai-weather-webhook-sample"
    )


if __name__ == '__main__':
    application = Application("/webhook", {
        "condition": [process_request]
    })
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port {0}".format(port))
    application.run('0.0.0.0', port, True)