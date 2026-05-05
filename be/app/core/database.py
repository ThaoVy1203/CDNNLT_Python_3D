import pymssql
from typing import Optional
from app.core.config import settings

class DatabaseConnection:
    _instance: Optional['DatabaseConnection'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self):
        try:
            conn = pymssql.connect(
                server=settings.DB_SERVER,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                as_dict=True  # Cần True để lấy kết quả dạng dict
            )
            return conn
        except pymssql.Error as e:
            raise Exception(f"Database connection failed: {str(e)}")
    
    def execute_query(self, query: str, params: tuple = ()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            # Với as_dict=True, fetchall() trả về list of dict
            results = cursor.fetchall()
            conn.commit()
            return results
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
