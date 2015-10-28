import json

class Config:

    _config = None

    @staticmethod
    def get(key):
        if not Config._config:
            with open("config.json") as config_str:
                Config._config = json.load(config_str)
        if not key:
            return Config._config
        return Config._config.get(key)
