import logging
import tornado.web
import DataAccess.DAFood
from BizModel.Entity import *
from Common.JsonEncoder import *
import traceback


class SaveFoodHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            params = self.request.arguments
            param_keys = params.keys()
            food_id = int(self.get_argument("food_id")) if 'food_id' in param_keys else None
            food_name = self.get_argument("food_name") if 'food_name' in param_keys else None
            brand_id = int(self.get_argument("brand_id")) if 'brand_id' in param_keys else None
            type_id = int(self.get_argument("type_id")) if 'type_id' in param_keys else None
            ingredient_ids = list(self.get_argument("ingredient_ids")) if 'ingredient_ids' in param_keys else None
            if food_name is None or len(food_name.strip()) == 0:
                raise CustomException('必须输入食品名')
            if brand_id is None:
                raise CustomException('必须输入食品品牌')
            if type_id is None:
                raise CustomException('必须输入食品类别')
            if ingredient_ids is None or len(ingredient_ids) == 0:
                raise CustomException('必须输入食品配料')
            if food_id is None:
                if DataAccess.DAFood.get_food_by_name(food_name) is not None:
                    raise CustomException('食品重复')
                result = DataAccess.DAFood.insert_food(food_name, brand_id, type_id, ingredient_ids)
            else:
                if DataAccess.DAFood.get_food(food_id) is None:
                    raise CustomException('食品不存在')
                else:
                    result = DataAccess.DAFood.update_food(food_id, food_name, brand_id, type_id, ingredient_ids)
            response.data = result
        except CustomException as cex:
            response.code = ResponseCode.ERROR
            response.error_message = str(cex)
            logging.info(str(cex))
        except Exception:
            response.code = ResponseCode.ERROR
            response.error_message = '保存食品发生异常'
            logging.error('保存食品发生异常:' + traceback.format_exc())
        self.write(json.dumps(response, cls=CustomEncoder, ensure_ascii=False))


class delete_food_handler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            food_id = int(self.get_argument("food_id"))
            response.data = DataAccess.DAFood.delete_food(food_id)
        except CustomException as cex:
            response.code = ResponseCode.ERROR
            response.error_message = str(cex)
            logging.info(str(cex))
        except Exception:
            response.code = ResponseCode.ERROR
            response.error_message = '删除食品发生异常'
            logging.error('删除食品发生异常:' + traceback.format_exc())
        self.write(json.dumps(response, cls=CustomEncoder, ensure_ascii=False))


class QueryFoodHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            params = self.request.arguments
            param_keys = params.keys()
            food_name = self.get_argument("food_name") if 'food_name' in param_keys else None
            page_index = int(self.get_argument("page_index")) if 'page_index' in param_keys else None
            page_size = int(self.get_argument("page_size")) if 'page_size' in param_keys else None
            order_by = self.get_argument("order_by") if 'order_by' in param_keys else None
            if page_index is None:
                response.data = DataAccess.DAFood.get_foods(food_name, None)
            else:
                page = PageEntity()
                page.page_size = page_size
                page.page_index = page_index
                page.order_by = order_by
                response.data = DataAccess.DAFood.get_foods(food_name, page)
                response.page_entity = page
        except CustomException as cex:
            response.code = ResponseCode.ERROR
            response.error_message = str(cex)
            logging.info(str(cex))
        except Exception:
            response.code = ResponseCode.ERROR
            response.error_message = '查询食品发生异常'
            logging.error('查询食品发生异常:' + traceback.format_exc())
        self.write(json.dumps(response, cls=CustomEncoder, ensure_ascii=False))
