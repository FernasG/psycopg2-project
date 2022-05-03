import psycopg2
from typing import Union

class DatabaseMananger:
    def __init__(self) -> None:
        self.__settings = {
            "password": "12345678",
            "dbname": "fernasdb",
            "user": "postgres",
            "host": "localhost"
        }

        self.__connection = psycopg2.connect(**self.__settings)
        self.__cursor = self.__connection.cursor()

    def find(self, query: str, limit: int = None) -> list:
        try:
            self.__cursor.execute(query)
            return self.__cursor.fetchmany(limit) if limit else self.__cursor.fetchall()
        except Exception as error:
            print(str(error))
            return False

    def findOne(self, query: str) -> tuple:
        try:
            self.__cursor.execute(query)
            return self.__cursor.fetchone()
        except Exception as error:
            print(str(error))
            return False

    def insert(self, query: str, values: Union[tuple, list], returning: bool = True) -> tuple:
        try:
            if returning: query = f"{query} RETURNING *"
            self.__cursor.execute(query, values)
            self.__connection.commit()
            return self.__cursor.fetchone() if returning else True
        except Exception as error:
            print(str(error))
            return False

    def close(self) -> None:
        self.__cursor.close()
        self.__connection.close()
        return
