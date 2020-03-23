import json


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'is_custom'):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
