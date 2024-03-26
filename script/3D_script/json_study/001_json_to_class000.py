import json
from pydantic import BaseModel

# 定义类
class User(BaseModel):
    id: int
    name:str
    sex:str
    age:int

    def myFunc(self):
        pass
# =======================================
# 字典数据
external_data = {
    'id': 1,
    'name':'周星驰',
    'sex':'男',
    'age':'18',
}


def dict_to_class(input_dict):
    result_class = User(**input_dict)
    return result_class

userClass = User(**external_data)
print(userClass.id)

# 类转字典数据
userDict = userClass.dict()
print(userDict)

userJson = json.dumps(userDict)
print(type(userJson))

userDict0 = json.loads(userJson)
print(type(userDict0))

