import pymysql


class ClassObject:
    className = ''
    school = ''

    def __init__(self, className):
        self.className = className

    def get_class_key(self):
        return self.className

    def set_class_attributes(self, school):
        self.school = school

    def generate_insert_string(self):
        sql = 'INSERT INTO thesis.class (ClassName, School) VALUES (%s,%s);'
        return sql

    def get_class(self, keyDevice):
        sql = "SELECT * FROM thesis.class where ClassName = %s;"
        cursor_local = self.connection_remote.cursor()
        cursor_local.execute(sql, keyDevice)
        for row in cursor_local:
            return row

    def generate_tuple(self):
        return (self.className, self.school)

    def sql_open(self):
        self.connection_remote = pymysql.connect(
            host="127.0.0.1",
            user="admin",
            passwd="lisonco20",
            database="thesis",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True)

    def insert_into_sql(self):
        cursor_local = self.connection_remote.cursor()
        cursor_local.execute(self.generate_insert_string(), self.generate_tuple())

    def sql_close(self):
        self.connection_remote.close()

if __name__ == '__main__':
    print('Create new Class')
    className = input('Class Name: ')
    school = input('School: ')

    obj = ClassObject(className)
    obj.set_class_attributes(school)
    obj.sql_open()
    obj.insert_into_sql()
    obj.sql_close()
