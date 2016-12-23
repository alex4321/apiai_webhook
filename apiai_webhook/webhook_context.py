class Context(object):
    def __init__(self, name, lifespan, parameters):
        """
        Initialize context object
        :param name: name
        :type name: str
        :param lifespan: lifespan
        :type lifespan: int
        :param parameters: parameters
        :type parameters: dict[str, str]
        """
        self.name = name
        self.lifespan = lifespan
        self.parameters = parameters
        super(Context, self).__init__()

    @staticmethod
    def from_dict(context):
        """
        Initialize context from dict
        :param context: context dict
        :type context: dict
        :return: context
        :rtype: Context
        """
        return Context(
            name=context.get("name", ""),
            lifespan=context.get("lifespan", 1),
            parameters=context.get("parameters", {})
        )

    @property
    def as_dict(self):
        return {
            "name": self.name,
            "lifespan": self.lifespan,
            "parameters": self.parameters
        }