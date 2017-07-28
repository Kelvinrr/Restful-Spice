import json

class BaseConfig(object):
    with open('available_missions.json', 'r') as f:
        AVAILABLE_MISSIONS = json.load(f)

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

class TestingConfig(BaseConfig):
    DEBUG = False
    Testing = True
