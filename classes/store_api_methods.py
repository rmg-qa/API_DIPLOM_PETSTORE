import requests
from jsonschema import validate
from schemas.schemas_response import get_the_number_of_pets_sold


class StoreApiMethods:
    @staticmethod
    def get_the_number_of_pets_sold(url):
        request = requests.get(f'{url}')
        validate(instance=request.json(), schema=get_the_number_of_pets_sold)
        return request
