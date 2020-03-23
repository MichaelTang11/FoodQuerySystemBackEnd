from Common.DBConnection import cursor
from DataAccess.DataModel import *
from BizModel.Entity import *
import math


def get_food(food_id: int):
    row_number = cursor.execute('SELECT * FROM tb_fqs_food WHERE id=%s', food_id)
    if row_number == 0:
        return None
    else:
        sql = '''
            SELECT 	T1.id AS 'food_id',
                    T1.food_name,
                    T1.brand_id,
                    T2.brand_name,
                    T1.type_id,
                    T3.type_name 
            FROM    tb_fqs_food T1 
                    LEFT JOIN tb_fqs_brand T2 ON T1.brand_id=T2.id
                    LEFT JOIN tb_fqs_type T3 ON T1.type_id=T3.id
            WHERE   T1.id=%s'''
        cursor.execute(sql, food_id)
        row = cursor.fetchone()
        food = FoodEntity()
        food.food_id = row['food_id']
        food.food_name = row['food_name']
        food.brand = TB_FQS_Brand(row['brand_id'], row['brand_name'])
        food.type = TB_FQS_Type(row['type_id'], row['type_name'])
        cursor.execute(
            '''
            SELECT 	T2.*
            FROM	tb_fqs_food_r_ingredient T1
                    LEFT JOIN tb_fqs_ingredient T2 ON T1.ingredient_id=T2.id
            WHERE T1.food_id=%s''',
            food.food_id
        )
        for row in cursor.fetchall():
            ingredient = TB_FQS_Ingredient(row['id'], row['ingredient_name'], row['ingredient_info'])
            food.ingredients.append(ingredient)
        return food


def get_food_by_name(food_name: str):
    row_number = cursor.execute('SELECT * FROM tb_fqs_food WHERE food_name=%s', food_name)
    if row_number == 0:
        return None
    else:
        sql = '''
                    SELECT 	T1.id AS 'food_id',
                            T1.food_name,
                            T1.brand_id,
                            T2.brand_name,
                            T1.type_id,
                            T3.type_name 
                    FROM    tb_fqs_food T1 
                            LEFT JOIN tb_fqs_brand T2 ON T1.brand_id=T2.id
                            LEFT JOIN tb_fqs_type T3 ON T1.type_id=T3.id
                    WHERE   T1.food_name=%s'''
        cursor.execute(sql, food_name)
        row = cursor.fetchone()
        food = FoodEntity()
        food.food_id = row['food_id']
        food.food_name = row['food_name']
        food.brand = TB_FQS_Brand(row['brand_id'], row['brand_name'])
        food.type = TB_FQS_Type(row['type_id'], row['type_name'])
        cursor.execute(
            '''
            SELECT 	T2.*
            FROM	tb_fqs_food_r_ingredient T1
                    LEFT JOIN tb_fqs_ingredient T2 ON T1.ingredient_id=T2.id
            WHERE T1.food_id=%s''',
            food.food_id
        )
        for row in cursor.fetchall():
            ingredient = TB_FQS_Ingredient(row['id'], row['ingredient_name'], row['ingredient_info'])
            food.ingredients.append(ingredient)
        return food


def get_foods(food_name: str, page_entity: PageEntity):
    if page_entity is None:
        page_entity = PageEntity()
        page_entity.page_index = 1
        page_entity.page_size = 20
        page_entity.order_by = 'T1.id'
    if food_name is None or len(food_name.strip()) == 0:
        sql = '''
                    SELECT 	T1.id AS 'food_id',
                            T1.food_name,
                            T1.brand_id,
                            T2.brand_name,
                            T1.type_id,
                            T3.type_name 
                    FROM    tb_fqs_food T1 
                            LEFT JOIN tb_fqs_brand T2 ON T1.brand_id=T2.id
                            LEFT JOIN tb_fqs_type T3 ON T1.type_id=T3.id {0} {1}'''.format(
            '' if len(page_entity.order_by.strip()) == 0 else 'ORDER BY ' + page_entity.order_by,
            '' if page_entity.page_size == 0 else 'LIMIT ' + str(
                (page_entity.page_index - 1) * page_entity.page_size) + ',' + str(page_entity.page_size)
        )
        row_number = cursor.execute(sql)
        if row_number == 0:
            return None
        else:
            result = []
            for row in cursor.fetchall():
                food = FoodEntity()
                food.food_id = row['food_id']
                food.food_name = row['food_name']
                food.brand = TB_FQS_Brand(row['brand_id'], row['brand_name'])
                food.type = TB_FQS_Type(row['type_id'], row['type_name'])
                cursor.execute(
                    '''
                    SELECT 	T2.*
                    FROM	tb_fqs_food_r_ingredient T1
                            LEFT JOIN tb_fqs_ingredient T2 ON T1.ingredient_id=T2.id
                    WHERE T1.food_id=%s''',
                    food.food_id
                )
                for _row in cursor.fetchall():
                    ingredient = TB_FQS_Ingredient(_row['id'], _row['ingredient_name'], _row['ingredient_info'])
                    food.ingredients.append(ingredient)
                result.append(food)
            cursor.execute('SELECT COUNT(0) AS number FROM tb_fqs_food')
            page_entity.total_row = cursor.fetchone()['number']
            if page_entity.page_size != 0:
                page_entity.page_count = math.ceil(page_entity.total_row / page_entity.page_size)
            return result
    else:
        sql = '''
            SELECT 	T1.id AS 'food_id',
                    T1.food_name,
                    T1.brand_id,
                    T2.brand_name,
                    T1.type_id,
                    T3.type_name 
            FROM    tb_fqs_food T1 
                    LEFT JOIN tb_fqs_brand T2 ON T1.brand_id=T2.id
                    LEFT JOIN tb_fqs_type T3 ON T1.type_id=T3.id 
            WHERE food_name LIKE %s {0} {1}'''.format(
            '' if len(page_entity.order_by.strip()) == 0 else 'ORDER BY ' + page_entity.order_by,
            '' if page_entity.page_size == 0 else 'LIMIT ' + str(
                (page_entity.page_index - 1) * page_entity.page_size) + ',' + str(page_entity.page_size)
        )
        row_number = cursor.execute(sql, '%' + food_name + '%')
        if row_number == 0:
            return None
        else:
            result = []
            for row in cursor.fetchall():
                food = FoodEntity()
                food.food_id = row['food_id']
                food.food_name = row['food_name']
                food.brand = TB_FQS_Brand(row['brand_id'], row['brand_name'])
                food.type = TB_FQS_Type(row['type_id'], row['type_name'])
                cursor.execute(
                    '''
                    SELECT 	T2.*
                    FROM	tb_fqs_food_r_ingredient T1
                            LEFT JOIN tb_fqs_ingredient T2 ON T1.ingredient_id=T2.id
                    WHERE T1.food_id=%s''',
                    food.food_id
                )
                for _row in cursor.fetchall():
                    ingredient = TB_FQS_Ingredient(_row['id'], _row['ingredient_name'], _row['ingredient_info'])
                    food.ingredients.append(ingredient)
                result.append(food)
            cursor.execute('SELECT COUNT(0) AS number FROM tb_fqs_food WHERE food_name LIKE %s', '%' + food_name + '%')
            page_entity.total_row = cursor.fetchone()['number']
            if page_entity.page_size != 0:
                page_entity.page_count = math.ceil(page_entity.total_row / page_entity.page_size)
            return result


def insert_food(food_name: str, brand_id: int, type_id: int, ingredient_ids: list):
    cursor.execute(
        '''INSERT INTO tb_fqs_food(`food_name`,`brand_id`,`type_id`) VALUES(%s,%s,%s);
        SELECT LAST_INSERT_ID() AS 'food_id' ''',
        (food_name, brand_id, type_id)
    )
    food_id = cursor.fetchone()['food_id']
    for ingredient_id in ingredient_ids:
        cursor.execute(
            'INSERT INTO tb_fqs_food_r_ingredient(`food_id`,`ingredient_id`) VALUES(%s,%s)',
            (food_id, ingredient_id)
        )
    return True


def update_food(food_id: int, food_name: str, brand_id: int, type_id: int, ingredient_ids: list):
    cursor.execute(
        'UPDATE tb_fqs_food SET food_name=%s,brand_id=%s,type_id=%s WHERE id=%s',
        (food_name, brand_id, type_id, food_id)
    )
    cursor.execute('DELETE FROM tb_fqs_food_r_ingredient WHERE food_id=%s', food_id)
    for ingredient_id in ingredient_ids:
        cursor.execute(
            'INSERT INTO tb_fqs_food_r_ingredient(`food_id`,`ingredient_id`) VALUES(%s,%s)',
            (food_id, ingredient_id)
        )
    return True


def delete_food(food_id: int):
    cursor.execute('DELETE FROM tb_fqs_food WHERE id=%s', food_id)
    cursor.execute('DELETE FROM tb_fqs_food_r_ingredient WHERE food_id=%s', food_id)
    return True
