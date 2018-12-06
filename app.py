from flask import Flask, request, url_for, render_template, make_response, redirect
import json

app = Flask(__name__,
    template_folder = "theme/template"
)

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    # print(request.cookies.get('username'))
    resp = make_response(
        render_template(
            'hello.html',
            name=name,
            WEBSITE_URL="http://localhost:5000/"
        )
    )
    resp.set_cookie('usernametwo', 'theusername')
    return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.json)
    print(request.args.get('bob'))

    if request.method == 'POST':
        return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    else:
        return "Show the login form"

app.run(debug=True)
