import json
from pydantic import BaseModel


def json_2_class(file_name: str):

    json.load(file_name)


