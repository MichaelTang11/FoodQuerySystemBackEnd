import logging
import tornado.web
import DataAccess.DAType
from BizModel.Entity import *
from Common.JsonEncoder import *
import traceback


class save_type_handler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            params = self.request.arguments
            param_keys = params.keys()
            type_id = int(self.get_argument("type_id")) if 'type_id' in param_keys else None
            type_name = self.get_argument("type_name") if 'type_name' in param_keys else None
            if type_name is None or len(type_name.strip()) == 0:
                raise CustomException('必须输入类型名')
            if type_id is None:
                if DataAccess.DAType.get_type_by_name(type_name) is not None:
                    raise CustomException('类型名重复')
                affected_rows = DataAccess.DAType.insert_type(type_name)
            else:
                if DataAccess.DAType.get_type(type_id) is None:
                    raise CustomException('类型不存在')
                else:
                    affected_rows = DataAccess.DAType.update_type(type_id, type_name)
            response.data = affected_rows
            logging.info('保存类型影响行数:' + str(affected_rows))
        except CustomException as cex:
            response.code = ResponseCode.ERROR
            response.error_message = str(cex)
            logging.info(str(cex))
        except Exception:
            response.code = ResponseCode.ERROR
            response.error_message = '保存类型发生异常'
            logging.error('保存类型发生异常:' + traceback.format_exc())
        self.write(json.dumps(response, cls=CustomEncoder, ensure_ascii=False))


class delete_type_handler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            type_id = int(self.get_argument("type_id"))
            affected_rows = DataAccess.DAType.delete_type(type_id)
            logging.info('删除类型影响行数:' + str(affected_rows))
            response.data = affected_rows
        except CustomException as cex:
            response.code = ResponseCode.ERROR
            response.error_message = str(cex)
            logging.info(str(cex))
        except Exception:
            response.code = ResponseCode.ERROR
            response.error_message = '删除类型发生异常'
            logging.error('删除类型发生异常:' + traceback.format_exc())
        self.write(json.dumps(response, cls=CustomEncoder, ensure_ascii=False))


class query_types_handler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        response = ResponseEntity()
        try:
            params = self.request.arguments
            param_keys = params.keys()
            type_name = self.get_argument("type_name") if 'type_name' in param_keys else None
            page_index = int(self.get_argument("page_index")) if 'page_index' in param_keys else None
            page_size = int(self.get_argument("page_size")) if 'page_size' in param_keys else None
            order_by = self.get_argument("order_by") if 'order_by' in param_keys else None
            if page_index is None:
                response.data = DataAccess.DAType.get_types(type_name, None)
            else:
                page = PageEntity()
                page.page_size = page_size
                page.page_index = page_index
                page.order_by = order_by
                response.data = DataAccess.DAType.get_types(type_name, page)
                response.page_entity = page
        except CustomException as cex:
            response.code = ResponseCode.ERROR
            response.error_message = str(cex)
            logging.info(str(cex))
        except Exception:
            response.code = ResponseCode.ERROR
            response.error_message = '查询类型发生异常'
            logging.error('查询类型发生异常:' + traceback.format_exc())
        self.write(json.dumps(response, cls=CustomEncoder, ensure_ascii=False))
