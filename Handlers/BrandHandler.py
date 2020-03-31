import logging
import tornado.web
from DataAccess import DABrand
from BizModel.Entity import *
from Common.JsonEncoder import *
from DataAccess.DataModel import *
import traceback


class save_brand_handler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            params = self.request.arguments
            param_keys = params.keys()
            brand_id = int(self.get_argument("brand_id")) if 'brand_id' in param_keys else None
            brand_name = self.get_argument("brand_name") if 'brand_name' in param_keys else None
            if brand_name is None or len(brand_name.strip()) == 0:
                raise CustomException('必须输入品牌名')
            if brand_id is None:
                if DABrand.get_brand_by_name(brand_name) is not None:
                    raise CustomException('品牌名重复')
                affected_rows = DABrand.insert_brand(brand_name)
            else:
                if DABrand.get_brand(brand_id) is None:
                    raise CustomException('品牌不存在')
                else:
                    affected_rows = DABrand.update_brand(brand_id, brand_name)
            response.data = affected_rows
            logging.info('保存品牌影响行数:' + str(affected_rows))
        except CustomException as cex:
            response.code = ResponseCode.ERROR.value
            response.error_message = cex.value
            logging.info(cex.value)
        except Exception:
            response.code = ResponseCode.ERROR.value
            response.error_message = '保存品牌发生异常'
            logging.error('保存品牌发生异常:' + traceback.format_exc())
        self.write(json.dumps(dict(response), ensure_ascii=False))


class delete_brand_handler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            brand_id = int(self.get_argument("brand_id"))
            affected_rows = DABrand.delete_brand(brand_id)
            logging.info('删除品牌影响行数:' + str(affected_rows))
            response.data = affected_rows
        except CustomException as cex:
            response.code = ResponseCode.ERROR.value
            response.error_message = cex.value
            logging.info(cex.value)
        except Exception:
            response.code = ResponseCode.ERROR.value
            response.error_message = '删除品牌发生异常'
            logging.error('删除品牌发生异常:' + traceback.format_exc())
        self.write(json.dumps(dict(response), ensure_ascii=False))


class query_brands_handler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            params = self.request.arguments
            param_keys = params.keys()
            brand_name = self.get_argument("brand_name") if 'brand_name' in param_keys else None
            page_index = int(self.get_argument("page_index")) if 'page_index' in param_keys else None
            page_size = int(self.get_argument("page_size")) if 'page_size' in param_keys else None
            order_by = self.get_argument("order_by") if 'order_by' in param_keys else None
            if page_index is None:
                response.data = DABrand.get_brands(brand_name, None)
            else:
                page = PageEntity()
                page.page_size = page_size
                page.page_index = page_index
                page.order_by = order_by
                response.data = DABrand.get_brands(brand_name, page)
                response.page_entity = page
        except CustomException as cex:
            response.code = ResponseCode.ERROR.value
            response.error_message = cex.value
            logging.info(cex.value)
        except Exception:
            response.code = ResponseCode.ERROR.value
            response.error_message = '查询品牌发生异常'
            logging.error('查询品牌发生异常:' + traceback.format_exc())
        self.write(json.dumps(dict(response), ensure_ascii=False))
