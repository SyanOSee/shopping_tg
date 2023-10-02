# Project
from panel import app, cf

if __name__ == '__main__':
    from uvicorn import run

    run(
        app,
        host=cf.server['host'],
        port=int(cf.server['port']),
    )
