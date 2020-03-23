from Common.DBConnection import cursor
from DataAccess.DataModel import TB_FQS_Brand
from BizModel.Entity import PageEntity
import math


def get_brand(brand_id: int):
    row_number = cursor.execute('SELECT * FROM tb_fqs_brand WHERE id=%s', brand_id)
    if row_number == 0:
        return None
    else:
        row = cursor.fetchone()
        return TB_FQS_Brand(row['id'], row['brand_name'])


def get_brand_by_name(brand_name: str):
    row_number = cursor.execute('SELECT * FROM tb_fqs_brand WHERE brand_name=%s', brand_name)
    if row_number == 0:
        return None
    else:
        row = cursor.fetchone()
        return TB_FQS_Brand(row['id'], row['brand_name'])


def get_brands(brand_name: str, page_entity: PageEntity):
    if page_entity is None:
        page_entity = PageEntity()
    if brand_name is None or len(brand_name.strip()) == 0:
        sql = 'SELECT * FROM tb_fqs_brand {0} {1}'.format(
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
                temp = TB_FQS_Brand(row['id'], row['brand_name'])
                result.append(temp)
            cursor.execute('SELECT COUNT(0) AS number FROM tb_fqs_brand')
            page_entity.total_row = cursor.fetchone()['number']
            if page_entity.page_size != 0:
                page_entity.page_count = math.ceil(page_entity.total_row / page_entity.page_size)
            return result
    else:
        sql = "SELECT * FROM tb_fqs_brand WHERE brand_name LIKE %s {0} {1}".format(
            '' if len(page_entity.order_by.strip()) == 0 else 'ORDER BY ' + page_entity.order_by,
            '' if page_entity.page_size == 0 else 'LIMIT ' + str(
                (page_entity.page_index - 1) * page_entity.page_size) + ',' + str(page_entity.page_size)
        )
        row_number = cursor.execute(sql, '%'+brand_name+'%')
        if row_number == 0:
            return None
        else:
            result = []
            for i in range(0, row_number):
                row = cursor.fetchone()
                temp = TB_FQS_Brand(row['id'], row['brand_name'])
                result.append(temp)
            cursor.execute('SELECT COUNT(0) AS number FROM tb_fqs_brand')
            page_entity.total_row = cursor.fetchone()['number']
            if page_entity.page_size != 0:
                page_entity.page_count = math.ceil(page_entity.total_row / page_entity.page_size)
            return result


def insert_brand(brand_name: str):
    return cursor.execute('INSERT INTO tb_fqs_brand(`brand_name`) VALUES(%s)', brand_name)


def update_brand(brand_id: int, brand_name: str):
    return cursor.execute('UPDATE tb_fqs_brand SET brand_name=%s WHERE id=%s', (brand_name, brand_id))


def delete_brand(brand_id: int):
    return cursor.execute('DELETE FROM tb_fqs_brand WHERE id=%s', brand_id)
