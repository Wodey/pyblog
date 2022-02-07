from flask import Flask

app = Flask(__name__)


@app.route("/")
def start():
    # This route return frontend interface
    pass


@app.route("/get_articles")
def get_articles(page):
    # This route returns list of articles for one of the pages
    # It returns only limited information required for displaying articles on the screen
    # It should return id, title, short description(just a few first paragraphs), data and tags of an article
    pass


@app.route("/get_article/id")
def get_article(id):
    # This route return a whole article
    # It gets an id of article
    # It returns id, title, markdown, data, tags
    pass


# These routes control authentication
@app.route("/admin/login", methods=["POST"])
def login():
    # This route control the login authentication
    # It receives a login and password of a user
    pass


@app.route("/admin/signup", methods=["POST"])
def signup():
    # This route let user signup for admin
    # but after that they cannot do anything
    # They need to get a permission from upper admin
    pass


@app.route("/admin/promote", methods=["POST"])
def promote():
    # This route let admin promote a user for higher permissions
    # It get a json body that consists from a user id and their
    # next rank 0 for usual user, rank 1 for editor, rank 2 for an admin
    # usual user can't do anything, editor can create, edit articles, admin can make all that can editor and promote
    # other people
    # These route requires the caller to be authorized for admin rank
    pass


# These routes are acceptable only for admin accounts
@app.route("/admin/make_an_article", methods=['POST'])
def make_an_article():
    # This route get a json body and add it to the database
    # Caller should be admin or editor
    # It returns 0 in success and 1 if it fails
    pass


@app.route("/admin/update_an_article", methods=['POST'])
def update_an_article():
    # This route receive a json body and update an article
    # Caller should be admin or editor
    # It returns 0 if it succeeds and 1 if it fails
    pass


@app.route("/admin/delete_an_article/id")
def delete_an_article(id):
    # This route get an id of article and delete it
    # Caller should be admin or editor
    # It returns 0 if it succeeds and 1 if it fails
    pass


if __name__ == '__main__':
    app.run()
