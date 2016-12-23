#!/usr/bin/env python

import os
import pyowm
import json
from apiai_webhook import Application, WebHookAnswer, WebHookRequest


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


def _get_conditions(city):
    observation = _owm().weather_at_place(city)
    if not observation:
        return None
    weather = observation.get_weather()
    if not weather:
        return None
    weather_info = {
        "clouds": weather.get_clouds(),
        "rain": weather.get_rain(),
        "snow": weather.get_snow(),
        "wind": weather.get_wind(),
        "humidity": weather.get_humidity(),
        "pressure": weather.get_pressure(),
        "status": weather.get_status()
    }
    return weather_info


def temperature_view(req):
    city = req.result.parameters.get("geo-city")
    temperature = _get_temperature(city)
    if not temperature:
        return WebHookAnswer()
    print("TEMPERATURE: ", city, temperature)
    if int(temperature[0]) != int(temperature[1]):
        speech = "{0}C - {1}C".format(temperature[0], temperature[1])
    else:
        speech = "{0}C".format(temperature[0])
    return WebHookAnswer(speech=speech, display_text=speech)


def conditions_view(req):
    city = req.result.parameters.get("geo-city")
    conditions = _get_conditions(city)
    if not conditions:
        return WebHookAnswer()
    print("CONDITIONS: ", city, conditions)
    speech = json.dumps(conditions, ensure_ascii=False)
    return WebHookAnswer(speech=speech, display_text=speech)


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
        "condition": [conditions_view]
    })
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port {0}".format(port))
    application.run('0.0.0.0', port, True)