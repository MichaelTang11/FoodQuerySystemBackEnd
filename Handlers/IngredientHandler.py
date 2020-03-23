import logging
import tornado.web
import DataAccess.DAIngredient
from BizModel.Entity import *
from Common.JsonEncoder import *
import traceback


class save_ingredient_handler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            params = self.request.arguments
            param_keys = params.keys()
            ingredient_id = int(self.get_argument("ingredient_id")) if 'ingredient_id' in param_keys else None
            ingredient_name = self.get_argument("ingredient_name") if 'ingredient_name' in param_keys else None
            if ingredient_name is None or len(ingredient_name.strip()) == 0:
                raise CustomException('必须输入配料名')
            ingredient_info = self.get_argument("ingredient_info") if 'ingredient_info' in param_keys else ''

            if ingredient_id is None:
                if DataAccess.DAIngredient.get_ingredient_by_name(ingredient_name) is not None:
                    raise CustomException('配料名重复')
                affected_rows = DataAccess.DAIngredient.insert_ingredient(
                    ingredient_name,
                    ingredient_info
                )
            else:
                if DataAccess.DAIngredient.get_ingredient(ingredient_id) is None:
                    raise CustomException('配料不存在')
                else:
                    affected_rows = DataAccess.DAIngredient.update_ingredient(
                        ingredient_id,
                        ingredient_name,
                        ingredient_info
                    )
            response.data = affected_rows
            logging.info('保存配料影响行数:' + str(affected_rows))
        except CustomException as cex:
            response.code = ResponseCode.ERROR
            response.error_message = str(cex)
            logging.info(str(cex))
        except Exception:
            response.code = ResponseCode.ERROR
            response.error_message = '保存配料发生异常'
            logging.error('保存配料发生异常:' + traceback.format_exc())
        self.write(json.dumps(response, cls=CustomEncoder, ensure_ascii=False))


class delete_ingredient_handler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            ingredient_id = int(self.get_argument("ingredient_id"))
            affected_rows = DataAccess.DAIngredient.delete_ingredient(ingredient_id)
            logging.info('删除配料影响行数:' + str(affected_rows))
            response.data = affected_rows
        except CustomException as cex:
            response.code = ResponseCode.ERROR
            response.error_message = str(cex)
            logging.info(str(cex))
        except Exception:
            response.code = ResponseCode.ERROR
            response.error_message = '删除配料发生异常'
            logging.error('删除配料发生异常:' + traceback.format_exc())
        self.write(json.dumps(response, cls=CustomEncoder, ensure_ascii=False))


class query_ingredients_handler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            params = self.request.arguments
            param_keys = params.keys()
            ingredient_name = self.get_argument("ingredient_name") if 'ingredient_name' in param_keys else None
            page_index = int(self.get_argument("page_index")) if 'page_index' in param_keys else None
            page_size = int(self.get_argument("page_size")) if 'page_size' in param_keys else None
            order_by = self.get_argument("order_by") if 'order_by' in param_keys else None
            if page_index is None:
                response.data = DataAccess.DAIngredient.get_ingredients(ingredient_name, None)
            else:
                page = PageEntity()
                page.page_size = page_size
                page.page_index = page_index
                page.order_by = order_by
                response.data = DataAccess.DAIngredient.get_ingredients(ingredient_name, page)
                response.page_entity = page
        except CustomException as cex:
            response.code = ResponseCode.ERROR
            response.error_message = str(cex)
            logging.info(str(cex))
        except Exception:
            response.code = ResponseCode.ERROR
            response.error_message = '查询配料发生异常'
            logging.error('查询配料发生异常:' + traceback.format_exc())
        self.write(json.dumps(response, cls=CustomEncoder, ensure_ascii=False))
