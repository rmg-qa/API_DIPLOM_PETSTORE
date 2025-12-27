import os

import dotenv
import allure
from classes.allure_attach import AllureLoggingMethods
from classes.store_api_methods import StoreApiMethods
from helpers import logging_helper

store = StoreApiMethods()
dotenv.load_dotenv()
base_url = os.getenv('URL')


@allure.story('Получение количества проданных домашних питомцев')
@allure.title('Получаем количество проданных домашних питомцев')
@allure.tag('api')
def test_get_the_number_of_pets_sold():
    with allure.step('Получаем количество проданных домашних питомцев'):
        response_get_the_number_of_pets_sold = store.get_the_number_of_pets_sold(url=base_url + '/store/inventory')
        logging_helper.log_2_console(response_get_the_number_of_pets_sold)
        AllureLoggingMethods.logging_response_json(response_get_the_number_of_pets_sold, name="Response")
        assert 'sold' in response_get_the_number_of_pets_sold.json()
        assert response_get_the_number_of_pets_sold.status_code == 200
