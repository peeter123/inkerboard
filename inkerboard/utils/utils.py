import json
import datetime
from dateutil import parser as date_parser
from json import JSONEncoder
from pathlib import Path


# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

    @staticmethod
    def decode_date_time(json_dict):
        if 'timestamp' in json_dict:
            json_dict["timestamp"] = date_parser.parse(json_dict["timestamp"])
            return json_dict


class Utils:
    @staticmethod
    def project_root() -> Path:
        return Path(__file__).parents[2]

    @staticmethod
    def serialize_json(data):
        return json.dumps(data, indent=4, cls=DateTimeEncoder)

    @staticmethod
    def deserialize_json(json_data):
        return json.loads(json_data, object_hook=DateTimeEncoder.decode_date_time)
