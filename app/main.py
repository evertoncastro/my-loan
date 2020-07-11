import os
import logging
from app import app
from api import load_api as load_loan_api


load_loan_api(app)


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    app.run(
        debug=False,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080))
    )
