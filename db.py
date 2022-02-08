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

    # Create a new Article
    def create_article(self, data: {}):
        cursor = self.connection.cursor()
        cursor.execute('USE PYBLOG')
        query = ('INSERT INTO Articles(title, description, content, date, author_id)'
                 'VALUES (%s, %s, %s, %s, %s)')

        cursor.execute(query, (data['title'], data['description'], data['content'], data['date'], data['author_id']))

        cursor.close()

    # It returns Article by id,
    # returns (id, title, description, content, date, author_id)
    def get_article(self, id: int) -> ():
        cursor = self.connection.cursor()
        cursor.execute('USE PYBLOG')
        query = f'SELECT * FROM ARTICLES WHERE id = {id}'
        cursor.execute(query)

        for i in cursor:
            result = i

        cursor.close()
        return result

    # It returns limited amount of articles for one page
    # returns [(id, title, description, date, author_id)]
    def get_articles(self, page: int) -> [()]:
        cursor = self.connection.cursor()
        cursor.execute('USE PYBLOG')

        start = (page-1) * 20

        query = f'SELECT id, title, description, date, author_id FROM Articles LIMIT {start}, 20'

        cursor.execute(query)

        result = []

        for i in cursor:
            result.append(i)

        cursor.close()
        return result

    def __delete__(self):
        self.connection.close()


if __name__ == "__main__":
    mydb = Db()
    print(mydb.get_article(1))
    print(mydb.get_articles(1))