from .webhook_context import Context


def _get(src, key, default):
    val = src.get(key)
    if val is not None:
        return val
    else:
        return default


class OriginalRequest(object):
    def __init__(self, request):
        """
        Initialize request
        :param request: request
        :type request: dict
        """
        self.source = _get(request, "source", "")
        data = _get(request, "data", {})
        self.text = _get(data, "text", "")
        self.match = _get(data, "match", [])
        self.type = _get(data, "type", "")
        self.event = _get(data, "event", "")
        self.team = _get(data, "team", "")
        self.user = _get(data, "user", "")
        self.channel = _get(data, "channel", "")
        self.ts = _get(data, "ts", "")
        super(OriginalRequest, self).__init__()


class Message(object):
    def __init__(self, message):
        """
        Initialize message
        :param message: message
        :type message: dict
        """
        self.speech = _get(message, "speech", "")
        self.type = _get(message, "type", 0)
        super(Message, self).__init__()


class Result(object):
    def __init__(self, result):
        """
        Initialize result
        :param result: result
        :type result: dict
        """
        self.speech = _get(result, "speech", "")
        self.score = _get(result, "score", 1.0)
        self.source = _get(result,"source", "")
        self.action = _get(result, "action", "")
        self.resolved_query = _get(result, "resolvedQuery", "")
        self.action_incomplete = _get(result, "actionIncomplete", False)
        self.contexts = [Context(context) for context in _get(result, "contexts", [])]
        self.parameters = _get(result, "parameters", {})
        self.metadata = _get(result, "metadata", {})
        fulfillment = _get(result, "fulfillment", {})
        self.fulfillment_speech = _get(fulfillment, "speech", "")
        self.fulfillment_messages = [Message(message)
                                     for message in _get(fulfillment, "messages", [])]
        super(Result, self).__init__()


class RequestStatus(object):
    def __init__(self, status):
        """
        Initialize status
        :param status: status
        :type status: dict
        """
        self.error_type = _get(status, "errorType", "success")
        self.code = _get(status, "code", 200)
        super(RequestStatus, self).__init__()


class WebHookRequest(object):
    def __init__(self, request):
        """
        Initialize request
        :param request: request
        :type request: dict
        """
        self.original_request = OriginalRequest(_get(request, "originalRequest", {}))
        self.timestamp = _get(request, "timestamp", "")
        self.result = Result(_get(request, "result", {}))
        self.session_id = _get(request, "sessionId", "")
        self.id = _get(request, "id", "")
        self.status = RequestStatus(_get(request, "status", {}))
        super(WebHookRequest, self).__init__()