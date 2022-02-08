from mysql.connector import connect, Error
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class Db:
    def __init__(self):
        try:
            self.connection = connect(
                host=getenv("DB_HOST"),
                user=getenv("DB_USER"),
                password=getenv("DB_PASSWORD")
            )
        except Error as e:
            print(e)


if __name__ == "__main__":
    mydb = Db()
