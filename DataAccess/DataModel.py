from BizModel.CustomObject import *


class TB_FQS_Brand(CustomObject):
    id = None
    brand_name = None

    def __init__(self, id, brand_name):
        self.id = id
        self.brand_name = brand_name

    def __str__(self):
        return '{' + '"id":{0},"brand_name":{1}'.format(
            str(self.id),
            '"' + self.brand_name + '"'
        ) + "}"

    def __repr__(self):
        return str(self)

    def keys(self):
        return 'id', 'brand_name'


class TB_FQS_Food(CustomObject):
    id = None
    food_name = None
    brand_id = None
    type_id = None

    def __init__(self, id, food_name, brand_id, type_id):
        self.id = id
        self.food_name = food_name
        self.brand_id = brand_id
        self.type_id = type_id

    def __str__(self):
        return '{' + '"id":{0},"food_name":{1},"brand_id":{2},"type_id":{3}'.format(
            str(self.id),
            '"' + self.food_name + '"',
            self.brand_id,
            str(self.type_id)
        ) + '}'

    def __repr__(self):
        return str(self)

    def keys(self):
        return 'id', 'food_name', 'brand_id', 'type_id'


class TB_FQS_Food_R_Ingredient(CustomObject):
    id = None
    food_id = None
    ingredient_id = None

    def __init__(self, id, food_id, ingredient_id):
        self.id = id
        self.food_id = food_id
        self.ingredient_id = ingredient_id

    def __str__(self):
        return '{' + '"id":{0},"brand_name":{1},"ingredient_id":{2}'.format(
            str(self.id),
            str(self.food_id),
            str(self.ingredient_id)
        ) + "}"

    def __repr__(self):
        return str(self)

    def keys(self):
        return 'id', 'food_id', 'ingredient_id'


class TB_FQS_Ingredient(CustomObject):
    id = None
    ingredient_name = None
    ingredient_info = None

    def __init__(self, id, ingredient_name, ingredient_info):
        self.id = id
        self.ingredient_name = ingredient_name
        self.ingredient_info = ingredient_info

    def __str__(self):
        return "{" + '"id":{0},"ingredient_name":{1},"ingredient_info":{2}'.format(
            str(self.id),
            '"' + str(self.ingredient_name) + '"',
            '"' + str(self.ingredient_info) + '"'
        ) + "}"

    def __repr__(self):
        return str(self)

    def keys(self):
        return 'id', 'ingredient_name', 'ingredient_info'


class TB_FQS_Type(CustomObject):
    id = None
    type_name = None

    def __init__(self, id, type_name):
        self.id = id
        self.type_name = type_name

    def __str__(self):
        return "{" + '"id":{0},"type_name":{1}'.format(
            str(self.id),
            '"' + str(self.type_name) + '"',
        ) + "}"

    def __repr__(self):
        return str(self)

    def keys(self):
        return 'id', 'type_name'
