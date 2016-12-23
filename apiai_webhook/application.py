import json
from flask import Flask, request, make_response
from .webhook_request import WebHookRequest
from .webhook_answer import WebHookAnswer


class Application(object):
    def __init__(self, route, handlers):
        """
        Initialize application
        :param route: route to webhook
        :type route: str
        :param handlers: action handlers
        :type handlers: dict[str, (WebHookRequest)->WebHookAnswer]
        """
        self.route = route
        self.flask = Flask(__name__)
        self._debug = False
        self.handlers = handlers

    def _action_handlers(self, action):
        """
        Get handlers for action
        :param action: action name
        :type action: str
        :return: handlers
        :rtype: list[(WebHookRequest)->WebHookAnswer]
        """
        handlers = []
        for handler_key in [action, ""]:
            handlers += self.handlers.get(handler_key, [])
        return handlers

    def handler(self):
        request_dict = request.get_json(silent=True, force=True)
        if self._debug:
            print("Request:")
            print(json.dumps(request_dict, indent=4))
        req = WebHookRequest(request_dict)
        handlers = self._action_handlers(req.result.action)
        result_dict = {}
        for handler in handlers:
            result = handler(req)
            result_dict = result.as_dict
            if result_dict != {}:
                break
        if self._debug:
            print("Answer:")
            print(json.dumps(request_dict, indent=4))
        response = make_response(result_dict)
        response.headers['Content-Type'] = 'application/json'
        return response


    def run(self, host='0.0.0.0', port=5000, debug=True):
        @self.flask.route(self.route, methods=['POST'])
        def _webhook():
            return self.handler()

        self._debug = debug
        self.flask.run(host, port, debug)