from sanic.blueprints import Blueprint
from sanic.response import json
from sanic_openapi import doc
from sanicargs import parse_parameters
from sanic.exceptions import SanicException
from sanic_jwt.decorators import protected

VALID_INPUT_TYPES = [int, float]

predictive_model = Blueprint("predictive_model", url_prefix="/v1/predictive_model")

async def execute_prediction(number_one, number_two):
    return (number_one*number_one) + (number_two*number_two)

async def validate_request_parameters(request):
    data = request.json
    number_one = data.get("n1")
    number_two = data.get("n2")
    if not number_one or not number_two:
        raise SanicException("Missing parameters, both 'n1' and 'n2' are needed", status_code=400)
    if type(number_one) not in VALID_INPUT_TYPES or type(number_two) not in VALID_INPUT_TYPES:
        raise SanicException("Type error, inputs 'n1' and 'n2' must be int or float", status_code=400)
    return number_one, number_two

@predictive_model.route("/", methods=['POST'])
@doc.summary("Predictive Model")
@doc.produces({"result": float})
@parse_parameters
@protected()
async def get_prediction(request):
    number_one, number_two = await validate_request_parameters(request)
    result = await execute_prediction(number_one, number_two)
    return json({"result": result})


