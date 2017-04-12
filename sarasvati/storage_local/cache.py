class StorageCache:
    def __init__(self):
        self.thoughts = {}
        self.lazy = {}

    def get(self, key):
        return self.thoughts.get(key, None)

    def add(self, thought, key=None, lazy=False):
        cache_key = key or thought.key
        self.thoughts[cache_key] = thought
        self.lazy[cache_key] = lazy

    def remove(self, thought):
        del self.thoughts[thought.key]
        del self.lazy[thought.key]

    def is_cached(self, key):
        return (key in self.thoughts) and not self.is_lazy(key)

    def is_cached_with_links(self, key):
        if self.is_cached(key):
            cached = self.get(key)
            if not self.has_lazy_children(cached):
                return self.get(key)

    def is_lazy(self, key):
        if key in self.lazy:
            return self.lazy[key]
        return False

    def has_lazy_children(self, thought):
        all_links = thought.links.all
        is_lazy_children = [self.is_lazy(x.key) for x in all_links]
        return sum(is_lazy_children) > 0

    def clear(self):
        self.thoughts.clear()
        self.lazy.clear()
