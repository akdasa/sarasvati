class Link:
    __VALID_LINK_KINDS = ["child", "parent", "reference"]

    def __init__(self, source, destination, kind):
        """
        Initializes new instance of the Link class.
        :type source: Thought
        :type destination: Thought
        :type kind: str
        :param source: Source
        :param destination: Destination
        :param kind: Kind of link
        """
        if kind not in self.__VALID_LINK_KINDS:
            raise ValueError("Invalid link kind: {}".format(kind))
        self.__source = source
        self.__destination = destination
        self.__kind = kind

    @property
    def source(self):
        return self.__source

    @property
    def destination(self):
        return self.__destination

    @property
    def kind(self):
        return self.__kind
