import pytest

@pytest.fixture(scope='function')
def app():
    from myfastapi import FastAPI
    return FastAPI()

@pytest.fixture(scope='function')
def client(app):
    from fastapi.testclient import TestClient
    return TestClient(app)