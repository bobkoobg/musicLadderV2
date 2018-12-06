from flask import Flask, request, url_for, render_template, make_response, redirect
import json

app = Flask(__name__,
    template_folder = "theme/template"
)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/helloalpha')
def helloalpha():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(">")
    print(request.json)
    print(request.args.get('bob'))

    if request.method == 'POST':
        return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    else:
        return "Show the login form"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    print(request.cookies.get('username'))

    resp = make_response(
        render_template(
            'hello.html',
            name=name,
            WEBSITE_URL="http://localhost:5000/"
        )
    )
    resp.set_cookie('usernametwo', 'theusername')
    return resp

# @app.route('/blobl')
# def index():
#     return redirect(url_for('/hello/'))


with app.test_request_context():
    url = url_for('static', filename='style.css')
    print(url)
#python -m flask run
#set FLASK_ENV=development / production (in terminal)
#set SERVER_NAME=bobbycom

app.run(debug=True)
