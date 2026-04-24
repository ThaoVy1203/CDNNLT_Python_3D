import pymssql
from typing import Optional
from .config import DatabaseConfig

class DatabaseConnection:
    _instance: Optional['DatabaseConnection'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self):
        try:
            conn = pymssql.connect(
                server=DatabaseConfig.SERVER,
                database=DatabaseConfig.DATABASE,
                user=DatabaseConfig.USERNAME,
                password=DatabaseConfig.PASSWORD,
                as_dict=False
            )
            return conn
        except pymssql.Error as e:
            raise Exception(f"Database connection failed: {str(e)}")
    
    def execute_query(self, query: str, params: tuple = ()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [column[0] for column in cursor.description] if cursor.description else []
            results = cursor.fetchall()
            conn.commit()  # Commit transaction for INSERT/UPDATE queries
            return [dict(zip(columns, row)) for row in results]
        finally:
            conn.close()
    
    def execute_non_query(self, query: str, params: tuple = ()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()
