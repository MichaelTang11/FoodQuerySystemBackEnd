import pymysql

con = pymysql.connect(
    host='127.0.0.1',
    user='root',
    port=3306,
    database='food_query_system',
    charset='utf8',
    password='usbw'
)
con.autocommit(1)
cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
