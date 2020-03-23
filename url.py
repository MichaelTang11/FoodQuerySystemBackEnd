from Handlers.BrandHandler import *
from Handlers.TypeHander import *
from Handlers.IngredientHandler import *
from Handlers.FoodHandler import *

url = {
    (r'/Brand/Save', save_brand_handler),
    (r'/Brand/Delete', delete_brand_handler),
    (r'/Brand/Query', query_brands_handler),

    (r'/Type/Save', save_type_handler),
    (r'/Type/Delete', delete_type_handler),
    (r'/Type/Query', query_types_handler),

    (r'/Ingredient/Save', save_ingredient_handler),
    (r'/Ingredient/Delete', delete_ingredient_handler),
    (r'/Ingredient/Query', query_ingredients_handler),

    (r'/Food/Save', save_ingredient_handler),
    (r'/Food/Delete', delete_ingredient_handler),
    (r'/Food/Query', query_ingredients_handler)
    # 测试路由
    # (r'/Test', TestHandler)
}
