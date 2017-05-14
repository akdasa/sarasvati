from abc import abstractmethod, ABCMeta


class Storage(metaclass=ABCMeta):
    @abstractmethod
    def add(self, thought):
        """
        Adds thought to storage
        :type thought: Thought
        :param thought: Thought
        """
        pass

    @abstractmethod
    def update(self, thought):
        """
        Updates thought
        :type thought: Thought
        :param thought: Thought to update 
        """
        pass

    @abstractmethod
    def remove(self, thought):
        """
        Removes thought from storage
        :type thought: Thought
        :param thought: Thought
        """
        pass

    @abstractmethod
    def search(self, query):
        """
        Search
        :param query: Query 
        :return: Array of thoughts if found 
        """
        pass

    @abstractmethod
    def get(self, key):
        """
        Returns thought by "identity.key"
        :param key: Key
        :return: Thought or None if nothing found
        """
        pass

    @abstractmethod
    def contains(self, key):
        """
        Returns True if storage contains thought with specified key
        :rtype: bool
        :type key: str
        :param key: Key
        :return: True if thought found in storage
        """
        pass

    @abstractmethod
    def count(self, query=None):
        """
        Returns count of Thoughts
        :type query: dict
        :rtype: int
        :param query: Query
        :return: Count
        """
        pass

    @property
    @abstractmethod
    def cache(self):
        """
        Returns cache
        """
        pass
