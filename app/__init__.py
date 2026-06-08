from flask import Flask

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'semag2026'

    from app.main.routes import main
    from app.usuario.routes import usuario

    app.register_blueprint(main)
    app.register_blueprint(usuario)

    return app 