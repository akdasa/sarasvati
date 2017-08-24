from sarasvati.exceptions import SarasvatiException


class Event:
    def __init__(self):
        """
        Initializes new instance of the Event class
        """
        self.handlers = []

    def subscribe(self, handler):
        """
        Subscribe for the event
        :param handler:
        """
        if handler not in self.handlers:
            self.handlers.append(handler)
        else:
            raise SarasvatiException("Already subscribed on specified handler")

    def unsubscribe(self, handler):
        """
        Unsubscribe from the event
        :param handler:
        """
        if handler in self.handlers:
            self.handlers.remove(handler)
        else:
            raise SarasvatiException("Not subscribed on specified handler")

    def notify(self, args):
        """
        Notify subscribers
        :param args: Event arguments
        """
        for handler in self.handlers:
            handler(args)
