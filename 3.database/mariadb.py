try:
    import pymysql
except:
    print('pip install pymysql 하세요')
import traceback
from typing import Union

class MariaDB:

    def __init__(self,db_config:dict,) -> None:
        """
        db_config = {
        host= '사용할 컴퓨터',
        user= '사용자 계정',
        password = '비밀번호'
        database= '사용할 데이터베이스',
        charset='utf8mb4' 
        )}
        """
        self.DB = pymysql.connect(**db_config)
    
    def __del__(self):
        """
        인스턴스 소멸 시 DB 연결 해제
        """
        self.DB.close()

    def select(self, column_qry:str, table:str, limit=None, offset=None, order_by=None, where_condition=[]) -> tuple:
        """
        Select

        ex) 
        column_qry = "*" : 모든열
        column_qry = "id, name, email" : 열이름
        table = "esg_project" : 테이블이름

        """

        sql_qr = "SELECT {0} FROM {1}".format(column_qry, table)
        if order_by:
            sql_qr += ' ORDER BY {}'.format(order_by)
        if limit:
            sql_qr += ' LIMIT {}'.format(limit)
        if offset:
            sql_qr += ' OFFSET {}'.format(offset)
        if where_condition:
            for i, (col, eq, val) in enumerate(where_condition):
                is_equal = '=' if eq else '!='
                is_multiple = ' AND' if i > 1 else ' WHERE'
                sql_qr += f'{is_multiple} {col}{is_equal}{val}'


        with self.DB.cursor() as cur:
            cur.execute(sql_qr)
            return cur.fetchall()
        

    def insert(self, table:str, columns: str, value: tuple) -> Union[int, bool]:
        """
        Insert Data
        
        example)
        table = "Students"
        columns = "name, email, phone"
        values = ('이름', '이메일', '번호')
        """

        sql_qr = f"INSERT INTO {table}({columns}) " \
                  "VALUES (" +','.join(["%s"]*len(value)) +")"
        # args = values
        
        try:
            with self.DB.cursor() as cur:
                cur.execute(sql_qr, value)
                self.DB.commit()
            return cur.lastrowid
        except:
            traceback.print_exc()
            self.DB.rollback()
            return False
    
    # values는 list 형식으로 넣었음, args로 함
    def insert_many(self, table:str, columns: str, values: list) -> bool:
        """
        Insert Many Datas
        
        example)
        table = "테이블이름"
        columns = "name, email, phone" 열이름들
        values = [
            ('hong gildong', 'hgd123@gmail.com', '01012345678'),
            ...
        ] 각 밸류 값들
        """
        sql = f"INSERT INTO {table}({columns}) " \
                  "VALUES ("  + ','.join(["%s"]*len(values[0])) + ");"
        try:
            with self.DB.cursor() as cur:
                cur.executemany(sql, values)
                self.DB.commit()
            return True
        except:
            traceback.print_exc()
            self.DB.rollback()
            return False
