import pytest


class MyPlugin:
    @staticmethod
    def pytest_sessionfinish():
        print("*** test run reporting finishing")

pytest.main(["-vv"], plugins=[MyPlugin()])
