import json
from enum import Enum, unique
from DataAccess.DataModel import *
from Common.JsonEncoder import *


class CustomObject:
    is_custom = True


@unique
class ResponseCode(Enum):
    SUCCESS = 200
    ERROR = 502


class PageEntity(CustomObject):
    page_index = 0
    page_size = 0
    page_count = 0
    total_row = 0
    order_by = ''

    def __str__(self):
        return "{'page_index':" + str(self.page_index) + ",'page_size':" + str(self.page_size) + ",'page_count':" + str(
            self.page_count) + ",'total_row':" + str(self.total_row) + ",'order_by':'" + self.order_by + "'}"


class ResponseEntity(CustomObject):
    code = ResponseCode.SUCCESS
    data = None
    error_message = None
    page_entity = PageEntity()

    def __str__(self):
        return "{" + "'code':{0},'data':{1},'error_message':{2},'page_entity':{3}".format(
            str(self.code.value),
            'null' if self.data is None else str(self.data),
            'null' if self.error_message is None else self.error_message,
            str(self.page_entity)
        ) + "}"


class CustomException(Exception, CustomObject):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FoodEntity(CustomObject):
    food_id = 0
    food_name = ''
    type = TB_FQS_Type(0, '')
    brand = TB_FQS_Brand(0, '')
    ingredients = []

    def __str__(self):
        return "{" + "'food_id':{0},'food_name':{1},'type':{2},'brand':{3},'ingredients':{4}".format(
            str(self.food_id),
            "'" + self.food_name + "'",
            json.dumps(self.type, cls=CustomEncoder, ensure_ascii=False),
            json.dumps(self.brand, cls=CustomEncoder, ensure_ascii=False),
            json.dumps(self.ingredients, cls=CustomEncoder, ensure_ascii=False)
        ) + "}"
