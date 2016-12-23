Intro
-----
This is wrapper to use with [api.ai](http://api.ai) service webhooks.
You can see example of usage for weather robot (with ```pyowl``` package to get weather data).

Concepts
--------
API.AI webhooks get "action" attribute.
This library filters handlers by action (you can use empty action name - "" - to handle all actions).

E.g.:

```
if __name__ == '__main__':
    application = Application("/webhook", {
        "temperature": [temperature_view],
        "conditions": [conditions_view],
    })
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port {0}".format(port))
    application.run('0.0.0.0', port, True)
```

Also, it's extract information from dicts (getted from API.AI) for input and store it in dict for output (for output).
So you'll work with request / answer as with other python objects
```
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
    speech = conditions["status"]
    return WebHookAnswer(speech=speech, display_text=speech)
```