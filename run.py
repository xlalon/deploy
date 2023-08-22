# -*- coding: utf8 -*-

from app import create_app

app = create_app()


@app.route('/ping')
def ping():
    return 'PONG!'


if __name__ == '__main__':
    app.run()
