import psycopg2

from os import environ
from typing import Union

class DatabaseMananger:
    def __init__(self) -> None:
        self.__settings = {
            "password": environ.get("DB_PASS"),
            "dbname": environ.get("DB_NAME"),
            "user": environ.get("DB_USER"),
            "host": environ.get("DB_HOST")
        }

        self.__connection = psycopg2.connect(**self.__settings)
        self.__cursor = self.__connection.cursor()

    def find(self, table: str, where: dict = None, select: list = None, limit: int = None) -> list:
        try:
            where, values = self.__setup_where(where) if where else ("1=1", None)
            select = ", ".join(select) if select else "*"
            query = f"SELECT {select} FROM {table} WHERE {where}"
            self.__cursor.execute(query, values)
            return self.__cursor.fetchmany(limit) if limit else self.__cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(str(error))
            return False

    def findOne(self, table: str, where: dict = None, select: list = None) -> tuple:
        try:
            where, values = self.__setup_where(where) if where else ("1=1", None)
            select = ", ".join(select) if select else "*"
            query = f"SELECT {select} FROM {table} WHERE {where}"
            self.__cursor.execute(query, values)
            return self.__cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            print(str(error))
            return False

    def insert(self, table: str, attrs: dict) -> tuple:
        try:
            if not attrs or not table: return False
            columns, values = self.__extract(attrs)
            query = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING *"
            result = self.__query(query, tuple(attrs.values()))
            return self.__cursor.fetchone() if result else result
        except (Exception, psycopg2.DatabaseError) as error:
            print(str(error))
            return False

    def update(self, query: str, values: Union[tuple, list]):
        return self.__query(query, values)

    def delete(self, query: str, values: Union[tuple, list]):
        return self.__query(query, values)

    def __query(self, query: str, values: Union[tuple, list]):
        try:
            self.__cursor.execute(query, values)
            self.__connection.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(str(error))
            self.__connection.rollback()
            return False

    def __extract(self, data: dict):
        columns = ", ".join(data.keys())
        values = ", ".join(["%s" for _ in range(len(data.keys()))])

        return columns, values

    def __setup_where(self, where: dict):
        sql = ", ".join([f"{key} = %s" for key in where.keys()])
        values = tuple(where.values())

        return sql, values

    def close(self) -> None:
        self.__cursor.close()
        self.__connection.close()
        return