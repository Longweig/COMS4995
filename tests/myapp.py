from flask import Flask


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    @app.route('/hello')
    def hello():
        return 'Hello, World!', 200

    @app.route('/')
    def base():
        return 'Success!', 200

    return app
