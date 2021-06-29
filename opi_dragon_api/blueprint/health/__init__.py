from sanic.blueprints import Blueprint
from sanic.response import json
from sanic_openapi import doc

health = Blueprint("health", url_prefix="/health")


@health.route("/status")
@doc.summary("Health Status, Health Check")
@doc.produces({"status": str})
async def health_status(request):
    return json({"status": "OK"})