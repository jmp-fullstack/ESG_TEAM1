try:
    import pymysql
except:
    print('you need to install pymysql\n$ : python -m pip install pymysql')
import traceback

from typing import Iterable, Union

class MariaDB:
    """
    MariaDB
    """

    def __init__(self, db_config:dict, cursor_type="tuple") -> None:
        """
        생성자 메서드
        인스턴스 생성 시 db_config를 전달받아 DB에 연결합니다.
        
        **db_config**
            host=database host (localhost)
            port=port (3306)
            user=username (root)
            password=password (1q2w3e)
            database=database name (testdb)
            charset=charcter encoding (utf8mb4)
        
        """

        db_config['port'] = int(db_config.get('port', '3306'))
        self.DB = pymysql.connect(**db_config)

        if cursor_type == 'dict':
            self.cursor_type = pymysql.cursors.DictCursor
        else:
            self.cursor_type = None
            
        return
    
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
