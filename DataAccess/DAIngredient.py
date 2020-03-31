from Common.DBConnection import cursor
from BizModel.Entity import *
import math
from DataAccess.DataModel import *


def get_ingredient(ingredient_id: int):
    row_number = cursor.execute('SELECT * FROM tb_fqs_ingredient WHERE id=%s', ingredient_id)
    if row_number == 0:
        return None
    else:
        row = cursor.fetchone()
        return TB_FQS_Ingredient(row['id'], row['ingredient_name'], row['ingredient_info'])


def get_ingredient_by_name(ingredient_name: str):
    row_number = cursor.execute('SELECT * FROM tb_fqs_ingredient WHERE ingredient_name=%s', ingredient_name)
    if row_number == 0:
        return None
    else:
        row = cursor.fetchone()
        return TB_FQS_Ingredient(row['id'], row['ingredient_name'], row['ingredient_info'])


def get_ingredients(ingredient_name: str, page_entity: PageEntity):
    if page_entity is None:
        page_entity = PageEntity()
    if ingredient_name is None or len(ingredient_name.strip()) == 0:
        sql = 'SELECT * FROM tb_fqs_ingredient {0} {1}'.format(
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
                temp = TB_FQS_Ingredient(row['id'], row['ingredient_name'], row['ingredient_info'])
                result.append(temp)
            cursor.execute('SELECT COUNT(0) AS number FROM tb_fqs_ingredient')
            page_entity.total_row = cursor.fetchone()['number']
            if page_entity.page_size != 0:
                page_entity.page_count = math.ceil(page_entity.total_row / page_entity.page_size)
            return result
    else:
        sql = "SELECT * FROM tb_fqs_ingredient WHERE ingredient_name LIKE %s {0} {1}".format(
            '' if len(page_entity.order_by.strip()) == 0 else 'ORDER BY ' + page_entity.order_by,
            '' if page_entity.page_size == 0 else 'LIMIT ' + str(
                (page_entity.page_index - 1) * page_entity.page_size) + ',' + str(page_entity.page_size)
        )
        row_number = cursor.execute(sql, '%' + ingredient_name + '%')
        if row_number == 0:
            return None
        else:
            result = []
            for i in range(0, row_number):
                row = cursor.fetchone()
                temp = TB_FQS_Ingredient(row['id'], row['ingredient_name'], row['ingredient_info'])
                result.append(temp)
            cursor.execute('SELECT COUNT(0) AS number FROM tb_fqs_ingredient')
            page_entity.total_row = cursor.fetchone()['number']
            if page_entity.page_size != 0:
                page_entity.page_count = math.ceil(page_entity.total_row / page_entity.page_size)
            return result


def insert_ingredient(ingredient_name: str, ingredient_info: str):
    return cursor.execute(
        'INSERT INTO tb_fqs_ingredient(`ingredient_name`,`ingredient_info`) VALUES(%s,%s)',
        (ingredient_name, ingredient_info)
    )


def update_ingredient(ingredient_id: int, ingredient_name: str, ingredient_info: str):
    return cursor.execute(
        'UPDATE tb_fqs_ingredient SET ingredient_name=%s,ingredient_info=%s WHERE id=%s',
        (ingredient_name, ingredient_info, ingredient_id)
    )


def delete_ingredient(ingredient_id: int):
    return cursor.execute('DELETE FROM tb_fqs_ingredient WHERE id=%s', ingredient_id)
