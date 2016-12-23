#!/usr/bin/env python

import os
import pyowm
from apiai_webhook import Application, WebHookAnswer, WebHookRequest


def temperature_view(req):
    city = req.result.parameters.get("geo-city")
    temperature = _get_temperature(city)
    if not temperature:
        return WebHookAnswer()
    print("TEMPERATURE: ", city, temperature)
    speech = "{0}C - {1}C".format(temperature[0], temperature[1])
    return WebHookAnswer(speech=speech, display_text=speech)


def _owm():
    api_key = os.getenv("OWM_API_KEY")
    return pyowm.OWM(api_key)


def _get_temperature(city):
    observation = _owm().weather_at_place(city)
    if not observation:
        return None
    weather = observation.get_weather()
    if not weather:
        return None
    temperature = weather.get_temperature('celsius')
    if not temperature:
        return None
    return temperature['temp_min'], temperature['temp_max']


#def make_webhook_result(data):
#    query = data.get('query')
#    print("QUERY : ", json.dumps(query))
#    if query is None:
#        return WebHookAnswer()
#    result = query.get('results')
#    print("RESULTS : ", json.dumps(result))
#    if result is None:
#        return WebHookAnswer()
#    channel = result.get('channel')
#    print("CHANNEL : ", json.dumps(channel))
#    if channel is None:
#        return WebHookAnswer()
#    item = channel.get('item')
#    print("ITEM : ", json.dumps(item))
#    location = channel.get('location')
#    print("LOCATION : ", json.dumps(location))
#    units = channel.get('units')
#    print("UNITS : ", json.dumps(units))
#    if (location is None) or (item is None) or (units is None):
#        return {}
#    condition = item.get('condition')
#    print("CONDITION : ", json.dumps(condition))
#    if condition is None:
#        return {}
#    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
#             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')
#    print("SPEECH : ", json.dumps(speech))
#    print("Response:")
#    print(speech)
#    return WebHookAnswer(
#        speech=speech,
#        display_text=speech,
#        source="apiai-weather-webhook-sample"
#    )


if __name__ == '__main__':
    application = Application("/webhook", {
        "condition": [temperature_view]
    })
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port {0}".format(port))
    application.run('0.0.0.0', port, True)