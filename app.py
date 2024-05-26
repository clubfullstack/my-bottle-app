from bottle import run, route

@route('/')
def home():
    return "<h1>Welcome to the homepage!</h1>"


run(debug=True, reloader=True)

