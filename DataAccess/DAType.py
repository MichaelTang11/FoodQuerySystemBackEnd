from Common.DBConnection import cursor
from DataAccess.DataModel import TB_FQS_Type
from BizModel.Entity import PageEntity
import math


def get_type(type_id: int):
    row_number = cursor.execute('SELECT * FROM tb_fqs_type WHERE id=%s', type_id)
    if row_number == 0:
        return None
    else:
        row = cursor.fetchone()
        return TB_FQS_Type(row['id'], row['type_name'])


def get_type_by_name(type_name: str):
    row_number = cursor.execute('SELECT * FROM tb_fqs_type WHERE type_name=%s', type_name)
    if row_number == 0:
        return None
    else:
        row = cursor.fetchone()
        return TB_FQS_Type(row['id'], row['type_name'])

def get_types(type_name: str, page_entity: PageEntity):
    if page_entity is None:
        page_entity = PageEntity()
    if type_name is None or len(type_name.strip()) == 0:
        sql = 'SELECT * FROM tb_fqs_type {0} {1}'.format(
            '' if len(page_entity.order_by.strip()) == 0 else 'ORDER BY ' + page_entity.order_by,
            '' if page_entity.page_size == 0 else 'LIMIT ' + str(
                (page_entity.page_index - 1) * page_entity.page_size) + ',' + str(page_entity.page_size)
        )
        row_number = cursor.execute(sql)
        if row_number == 0:
            return None
        else:
            result = []
            for i in range(0, row_number):
                row = cursor.fetchone()
                temp = TB_FQS_Type(row['id'], row['type_name'])
                result.append(temp)
            cursor.execute('SELECT COUNT(0) AS number FROM tb_fqs_type')
            page_entity.total_row = cursor.fetchone()['number']
            if page_entity.page_size != 0:
                page_entity.page_count = math.ceil(page_entity.total_row / page_entity.page_size)
            return result
    else:
        sql = "SELECT * FROM tb_fqs_type WHERE type_name LIKE %s {0} {1}".format(
            '' if len(page_entity.order_by.strip()) == 0 else 'ORDER BY ' + page_entity.order_by,
            '' if page_entity.page_size == 0 else 'LIMIT ' + str(
                (page_entity.page_index - 1) * page_entity.page_size) + ',' + str(page_entity.page_size)
        )
        row_number = cursor.execute(sql, '%'+type_name+'%')
        if row_number == 0:
            return None
        else:
            result = []
            for i in range(0, row_number):
                row = cursor.fetchone()
                temp = TB_FQS_Type(row['id'], row['type_name'])
                result.append(temp)
            cursor.execute('SELECT COUNT(0) AS number FROM tb_fqs_type')
            page_entity.total_row = cursor.fetchone()['number']
            if page_entity.page_size != 0:
                page_entity.page_count = math.ceil(page_entity.total_row / page_entity.page_size)
            return result


def insert_type(type_name: str):
    return cursor.execute('INSERT INTO tb_fqs_type(`type_name`) VALUES(%s)', type_name)


def update_type(type_id: int, type_name: str):
    return cursor.execute('UPDATE tb_fqs_type SET type_name=%s WHERE id=%s', (type_name, type_id))


def delete_type(type_id: int):
    return cursor.execute('DELETE FROM tb_fqs_type WHERE id=%s', type_id)
