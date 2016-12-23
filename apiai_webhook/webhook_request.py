from .webhook_context import Context


class OriginalRequest(object):
    def __init__(self, request):
        """
        Initialize request
        :param request: request
        :type request: dict
        """
        self.source = request.get("source", "")
        data = request.get("data", {})
        self.text = data.get("text", "")
        self.match = data.get("match", [])
        self.type = data.get("type", "")
        self.event = data.get("event", "")
        self.team = data.get("team", "")
        self.user = data.get("user", "")
        self.channel = data.get("channel", "")
        self.ts = data.get("ts", "")
        super(OriginalRequest, self).__init__()


class Message(object):
    def __init__(self, message):
        """
        Initialize message
        :param message: message
        :type message: dict
        """
        self.speech = message.get("speech", "")
        self.type = message.get("type", 0)
        super(Message, self).__init__()


class Result(object):
    def __init__(self, result):
        """
        Initialize result
        :param result: result
        :type result: dict
        """
        self.speech = result.get("speech")
        self.score = result.get("score", 1.0)
        self.source = result.get("source", "")
        self.action = result.get("action", "")
        self.resolved_query = result.get("resolvedQuery", "")
        self.action_incomplete = result.get("actionIncomplete", False)
        self.contexts = [Context(context) for context in result.get("contexts", [])]
        self.parameters = result.get("parameters", {})
        self.metadata = result.get("metadata", {})
        fulfillment = result.get("fulfillment", {})
        self.fulfillment_speech = fulfillment.get("speech", "")
        self.fulfillment_messages = [Message(message)
                                     for message in fulfillment.get("messages", [])]
        super(Result, self).__init__()


class RequestStatus(object):
    def __init__(self, status):
        """
        Initialize status
        :param status: status
        :type status: dict
        """
        self.error_type = status.get("errorType", "success")
        self.code = status.get("code", 200)
        super(RequestStatus, self).__init__()


class WebHookRequest(object):
    def __init__(self, request):
        """
        Initialize request
        :param request: request
        :type request: dict
        """
        self.original_request = OriginalRequest(request.get("originalRequest", {}))
        self.timestamp = request.get("timestamp", "")
        self.result = Result(request.get("result", {}))
        self.session_id = request.get("sessionId", "")
        self.id = request.get("id", "")
        self.status = RequestStatus(request.get("status", {}))
        super(WebHookRequest, self).__init__()