from sarasvati.brain import Thought


class StorageCache:
    """Storage cache"""
    def __init__(self):
        """
        Initializes new instance of the StorageCache class.
        """
        self.thoughts = {}
        self.lazy = {}

    def get(self, key):
        """
        Returns thought by key, None if nothong found
        :type key: str
        :rtype: Thought
        :param key: Key
        :return: Thought 
        """
        return self.thoughts.get(key, None)

    def add(self, thought, lazy=False):
        """
        Adds thought to cache
        :type lazy: bool
        :type thought: Thought
        :param thought: Thought
        :param lazy: Is thought lazy?
        """
        self.thoughts[thought.key] = thought
        self.lazy[thought.key] = lazy

    def remove(self, thought):
        """
        Remove thought from cache
        :type thought: Thought
        :param thought: Thought
        """
        del self.thoughts[thought.key]
        del self.lazy[thought.key]

    def is_cached(self, key):
        """
        Is thought cached?
        :rtype: bool
        :type key: str
        :param key: Key
        :return: True if thought cached
        """
        return key in self.thoughts

    def is_lazy(self, key):
        """
        Is thought lazy?
        :rtype: bool
        :param key: Key
        :return: True if thought lazy
        """
        return self.lazy.get(key, False)

    def is_cached_with_links(self, key):
        """
        Is thought cached with all linked thoughts?
        :rtype: bool
        :type key: str
        :param key: Key
        :return: True if thought and all linked thoughts are cached
        """
        cached = self.get(key)
        if cached and not self.has_lazy_children(cached):
            return self.get(key)

    def has_lazy_children(self, thought):
        """
        Has specified thought lazy links?
        :param thought: Thought
        :return: True, if one ot linked thoughts is lazy
        """
        all_links = thought.links.all
        is_lazy_children = [self.is_lazy(x.key) for x in all_links]
        return sum(is_lazy_children) > 0

    def clear(self):
        """
        Clears cache
        """
        self.thoughts.clear()
        self.lazy.clear()
