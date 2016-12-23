from .webhook_context import Context


class WebHookAnswer(object):
    def __init__(self, speech="", display_text="", data={}, context_out=[], source=""):
        """
        Initialize webhook answer
        :param speech: Voice response to the request
        :param display_text: Text displayed on the user device screen
        :param data: Additional data required for performing the action on the client side. \
            The data is sent to the client in the original form and is not processed by API.AI.
        :param context_out: Array of context objects set after intent completion
        :type context_out: list[Context]
        :param source: Data source
        :type source: str
        """
        self.speech = speech
        self.display_text = display_text
        self.data = data
        self.context_out = context_out
        self.source = source
        super(WebHookAnswer, self).__init__()

    @property
    def as_dict(self):
        return {
            "speech": self.speech,
            "displayText": self.display_text,
            "contextOut": [item.as_dict for item in self.context_out],
            "source": self.source
        }