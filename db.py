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
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('USE PYBLOG')
                query = ('INSERT INTO Articles(title, description, content, date, author_id)'
                         'VALUES (%s, %s, %s, %s, %s)')

                cursor.execute(query, (data['title'], data['description'], data['content'], data['date'], data['author_id']))

                self.connection.commit()

                return 0
        except Error as err:
            print(err)
            return 1

    # It returns Article by id,
    # returns (id, title, description, content, date, author_id)
    def get_article(self, id: int) -> ():
        cursor = self.connection.cursor()
        cursor.execute('USE PYBLOG')
        query = f'SELECT * FROM ARTICLES WHERE id = {id}'
        cursor.execute(query)

        result = None
        for i in cursor:
            result = i

        cursor.close()
        return result

    # It returns limited amount of articles for one page
    # returns [(id, title, description, date, author_id)]
    def get_articles(self, page: int) -> [()]:
        cursor = self.connection.cursor()
        cursor.execute('USE PYBLOG')

        start = (page - 1) * 20

        query = f'SELECT id, title, description, date, author_id FROM Articles LIMIT {start}, 20'

        cursor.execute(query)

        result = []

        for i in cursor:
            result.append(i)

        cursor.close()
        return result

    # 0 if it succeeds, 1 if it fails
    def update_article(self, id: int, data: {}) -> int:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('USE PYBlOG')

                query = f'UPDATE Articles SET '
                for i in data:
                    query += f'{i} = "{data[i]}", '
                query = query[:-2]
                query += f'WHERE id = {id}'

                cursor.execute(query)

                self.connection.commit()

                return 0
        except Error as e:
            print(e)
            return 1

    # 1 if it fails and 0 if it succeeds
    def delete_article(self, id: int) -> int:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('USE PYBLOG')

                query = 'DELETE FROM ARTICLES WHERE id = %s'

                cursor.execute(query, (id,))

                self.connection.commit()
                return 0

        except Error as e:
            print(e)
            return 1

    # 1 if it fails and 0 if it succeeds
    def create_user(self, data: {}) -> int:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('USE PYBLOG')

                query = 'INSERT INTO Users(username, password, role) ' \
                        'VALUES (%s, %s, %s)'

                cursor.execute(query, (data['username'], data['password'], data['role']))

                self.connection.commit()

                return 0

        except Error as err:
            print(err)
            return 1

    # 1 if it fails and a user if it succeeds
    def get_user(self, username: str) -> ():
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('USE PYBLOG')

                query = 'SELECT * FROM Users WHERE username = %s'

                cursor.execute(query, (username,))

                result = None
                for i in cursor:
                    result = i

                return result
        except Error as err:
            print(err)
            return 1

    # 1 if it fails and 0 if it succeeds
    def promote_user(self, id: int, new_role: int) -> int:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('USE PYBLOG')

                query = f'UPDATE Users ' \
                        'SET role = %s ' \
                        'WHERE id = %s'

                cursor.execute(query, (new_role, id))

                self.connection.commit()

                return 0

        except Error as err:
            print(err)
            return 1

        # 1 if it fails and 0 if it succeeds

    def delete_user(self, id: int) -> int:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('USE PYBLOG')

                query = 'DELETE FROM USERS WHERE id = %s'

                cursor.execute(query, (id,))

                self.connection.commit()
                return 0

        except Error as e:
            print(e)
            return 1

    def __delete__(self):
        self.connection.close()


if __name__ == "__main__":
    mydb = Db()
    mydb.create_user({'username': 'testuser', 'password': 'password', 'role': 0})
    print(mydb.get_user('testuser'))
    print(mydb.get_user('ivan'))
    print(mydb.promote_user(2, 3))
    print(mydb.get_user('olia'))
    print(mydb.delete_user(4))
    # TEST NEW USER FUNCTIONS TOMMOROW
