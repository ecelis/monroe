from flask import Flask
import monroe

api = Flask(__name__)

@api.route('/')
def aping():
    return 'v0.1'


@api.route('/start')
def start_monroe():
    monroe.main()
