from opi_dragon_api.opi_dragon_api import app
from opi_dragon_api.util import sanic_config_manager


# from opi_dragon_api.plugin.opentracing import setup_opentracing

# setup_opentracing(app=app)



sanic_config_manager(app, prefix="SANIC_")


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8000, workers=4)

