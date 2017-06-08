_api_instance = None


def get_api():
    return _api_instance


def set_api(value):
    global _api_instance
    _api_instance = value
