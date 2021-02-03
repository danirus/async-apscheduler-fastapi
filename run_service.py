import logging.config

from app.config import LOGGING


if __name__ == '__main__':
    import uvicorn
    from app.main import app
    logging.config.dictConfig(LOGGING)
    uvicorn.run(app, host="localhost", port=8010)
