from sanic import Sanic
from sanic.response import json
from sanic_openapi import swagger_blueprint
from sanic_cors import CORS
from sanic_jwt import Initialize

from opi_dragon_api.auth import my_authenticate
from opi_dragon_api.blueprint.health import health
from opi_dragon_api.blueprint.predictive_model import predictive_model
from opi_dragon_api.util import setup_rate_limiter


app = Sanic(__name__)

limiter = setup_rate_limiter(app)
limiter.limit("3 per minute")(predictive_model)
limiter.limit("1000 per month")(predictive_model)

app.blueprint(swagger_blueprint)
app.blueprint(health)
app.blueprint(predictive_model)

Initialize(
    app,
    authenticate=my_authenticate,
)


@app.route("/")
async def default(request):
    return json({"message": "OPI Dragon API working fine!"})
