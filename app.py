from flask import Flask, request
from db import Db
import hashlib
import binascii

app = Flask(__name__)

db = Db()

salt = 21


@app.route("/")
def start():
    # This route return frontend interface
    pass


@app.route("/get_articles/<int:page>")
def get_articles(page):
    """
    This route returns list of articles for one of the pages
    It returns only limited information required for displaying articles on the screen
    It should return id, title, short description(just a few first paragraphs), data and tags of an article

    """
    raw_articles = db.get_articles(page)
    result = []

    for i in raw_articles:
        result.append({
            "id": i[0],
            "title": i[1],
            "description": i[2],
            "date": i[3],
            "author_id": i[4]
        })

    return {
        "articles": result
    }


@app.route("/get_article/<int:id>")
def get_article(id):
    """
    This route return a whole article
    It gets an id of article
    It returns id, title, markdown, data, tags

    """
    raw_article = db.get_article(id)

    return {
        "article": {
            "id": raw_article[0],
            "title": raw_article[1],
            "description": raw_article[2],
            "content": raw_article[3],
            "date": raw_article[4],
            "author_id": raw_article[5]
        }
    }


# These routes control authentication
@app.route("/admin/login", methods=["POST"])
def login():
    """
    This route control the login authentication
    It receives a login and password of a user

    """
    pass


@app.route("/admin/signup", methods=["POST"])
def signup():
    """
    This route let user signup for admin
    but after that they cannot do anything
    They need to get a permission from upper admin

    """
    body = request.get_json()

    for i in {"username", "password"}:
        if not i in body:
            return f"There is no {i} field in body"

    hashed_password = hashlib.pbkdf2_hmac('sha256', body['password'].encode('utf-8'), salt.to_bytes(2, byteorder='big'),
                                          10000)

    return str(db.create_user({'username': body['username'], 'password': binascii.hexlify(hashed_password), 'role': 1}))


@app.route("/admin/promote", methods=["POST"])
def promote():
    """
    This route let admin promote a user for higher permissions
    next rank 0 for usual user, rank 1 for editor, rank 2 for an admin
    usual user can't do anything, editor can create, edit articles, admin can make all that can editor and promote
    other people
    These route requires the caller to be authorized for admin rank

    """
    body = request.get_json()

    fields = {'uid', 'new_role'}

    for i in fields:
        if not i in body:
            return f"There is no {i} fields in body"

    if not body['new_role'] in {1, 2, 3}:
        return "The new_role field should be 1,2 or 3"

    return str(db.promote_user(body['uid'], body['new_role']))


# These routes are acceptable only for admin accounts
@app.route("/admin/make_article", methods=['POST'])
def make_article():
    """
    This route get a json body and add it to the database
    Caller should be admin or editor
    It returns 0 in success and 1 if it fails

    """
    body = request.get_json()

    fields = {'title', 'description', 'date', 'author_id', 'content'}

    for i in fields:
        if not i in body:
            return f'There is no field {i} in the body'

    return str(db.create_article(body))


@app.route("/admin/update_article", methods=['POST'])
def update_article():
    """
    This route receive a json body and update an article
    Caller should be admin or editor
    It returns 0 if it succeeds and 1 if it fails
    It gets body { id: ..., update: {...} }

    """
    body = request.get_json()

    if not body.get('update') or len(body.get('update').keys()) < 1:
        return "Please, provide at least 1 field to change"

    if not body.get('id'):
        return "Please, provide an id of Artilce to be changed"

    return str(db.update_article(body['id'], body['update']))


@app.route("/admin/delete_article/<int:id>")
def delete_article(id):
    """
    This route get an id of article and delete it
    Caller should be admin or editor
    It returns 0 if it succeeds and 1 if it fails

    """
    return str(db.delete_article(id))


@app.route("/admin/delete_user/<int:id>")
def delete_user(id):
    """
    This route deletes the user by id
    It returns 0 if it succeeds and 1 if it fails

    """
    return str(db.delete_user(id))


if __name__ == '__main__':
    app.run(debug=True)
