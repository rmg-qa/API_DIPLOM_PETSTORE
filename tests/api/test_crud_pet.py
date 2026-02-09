import os

import dotenv
import allure
import pytest
import requests

from classes.allure_attach import AllurePetLoggingMethods
from classes.allure_attach import AllureLoggingMethods
from classes.pet_api_methods import PetApiMethods
from helpers import logging_helper

pet = PetApiMethods()
dotenv.load_dotenv()
base_url = os.getenv('URL')


@allure.story('Получение питомцев по определенному статусу: "available", "pending", "sold"')
@allure.title('Получение питомцев по статусу')
@allure.tag('api')
@pytest.mark.parametrize('status', ["available", "pending", "sold"])
def test_get_pets_by_status(status):
    params = {"status": status}
    response = pet.get_pets(base_url + '/pet' + '/findByStatus', params=params)
    AllureLoggingMethods.logging_response_json(result=response, name="Response body")
    logging_helper.log_2_console(response, params)
    assert response.status_code == 200
    assert response.json()[0]['status'] == status


@allure.story('Создание питомца')
@allure.title('Создаем питомца и проверяем, что питомец создался корректно.')
@allure.tag('api')
def test_create_pet(generate_payload):
    with allure.step('Создаем питомца'):
        AllureLoggingMethods.logging_request_json(request_body=generate_payload, name='Request')
        response_create_pet = pet.create_pet(url=base_url + '/pet', payload=generate_payload)
        logging_helper.log_2_console(response_create_pet)
        AllureLoggingMethods.logging_response_json(response_create_pet, name="Response")
    with allure.step('Получаем созданного питомца по его id'):
        id_new_pet = response_create_pet.json()['id']
        response_get_a_created_pet = pet.get_pet_id(url=base_url + '/pet', id_pet=id_new_pet)
        logging_helper.log_2_console(response_get_a_created_pet)
        AllureLoggingMethods.logging_response_json(response_get_a_created_pet, name="Response")
    assert response_create_pet.status_code == 200
    assert response_get_a_created_pet.status_code == 200
    assert response_get_a_created_pet.json() == generate_payload
    with allure.step('Удаляем созданного питомца'):
        response_delete_pet = pet.delete_pet(url=base_url + '/pet', id_pet=id_new_pet)
        logging_helper.log_2_console(response_delete_pet)
        AllurePetLoggingMethods.logging_delete_pet(id_pet=id_new_pet, result=response_delete_pet, name='Response')
    assert response_delete_pet.status_code == 200
    assert response_delete_pet.json()['message'] == str(id_new_pet)


@allure.story('Изменение параметров питомца')
@allure.title('Создаем питомца и меняем ему имя.')
@allure.tag('api')
def test_update_pet(generate_payload):
    with allure.step('Создаем питомца'):
        AllureLoggingMethods.logging_request_json(request_body=generate_payload, name='Request')
        response_create_pet = pet.create_pet(url=base_url + '/pet', payload=generate_payload)
        logging_helper.log_2_console(response_create_pet)
        AllureLoggingMethods.logging_response_json(response_create_pet, name="Response")
    with allure.step('Получаем id созданного питомца, передаем его в PUT-запрос'):
        id_new_pet = response_create_pet.json()['id']
        update_data = {"name": 'AQA'}
        response_update_pet = pet.update_pet(url=base_url + '/pet', id_pet=id_new_pet, data=update_data)
        logging_helper.log_2_console(response_update_pet)
        AllureLoggingMethods.logging_response_json(response_update_pet, name="Response")
    with allure.step('Получаем имя питомца и сравниаем его с измененным значением'):
        response_get_pet_id = pet.get_pet_id(base_url + '/pet', id_new_pet)
        pet_name = response_get_pet_id.json()['name']
        logging_helper.log_2_console(response_get_pet_id)
        AllureLoggingMethods.logging_response_json(response_get_pet_id, name="Response")
        assert response_get_pet_id.status_code == 200
        assert pet_name == update_data['name']
    with allure.step('Удаляем созданного питомца'):
        response_delete_pet = pet.delete_pet(url=base_url + '/pet', id_pet=id_new_pet)
        logging_helper.log_2_console(response_delete_pet)
        AllurePetLoggingMethods.logging_delete_pet(id_pet=id_new_pet, result=response_delete_pet, name='Response')
        assert response_delete_pet.status_code == 200
        assert response_delete_pet.json()['type'] == 'unknown'
        assert response_delete_pet.json()['message'] == str(id_new_pet)


@allure.story('Удаление питомца')
@allure.title('Проверка удаления питомца')
@allure.tag('api')
def test_delete_pet(generate_payload):
    with allure.step('Создаем питомца и получаем его id'):
        AllureLoggingMethods.logging_request_json(request_body=generate_payload, name='Request')
        response_create_pet = pet.create_pet(url=base_url + '/pet', payload=generate_payload)
        logging_helper.log_2_console(response_create_pet)
        AllureLoggingMethods.logging_response_json(response_create_pet, name="Response")
        id_new_pet = response_create_pet.json()['id']
    with allure.step('Удаляем созданного питомца'):
        response_delete_pet = pet.delete_pet(url=base_url + '/pet', id_pet=id_new_pet)
        logging_helper.log_2_console(response_delete_pet)
        AllurePetLoggingMethods.logging_delete_pet(id_pet=id_new_pet, result=response_delete_pet, name='Response')
        assert response_delete_pet.status_code == 200
        assert response_delete_pet.json()['type'] == 'unknown'
        assert response_delete_pet.json()['message'] == str(id_new_pet)
    with allure.step('Проверяем, что питомец точно удалился'):
        repeat_the_deletion_of_the_created_pet = pet.delete_pet(url=base_url + '/pet', id_pet=id_new_pet)
        logging_helper.log_2_console(repeat_the_deletion_of_the_created_pet)
        assert repeat_the_deletion_of_the_created_pet.status_code == 404


@allure.title('test api')
def test_api_on_new_jenkins():
    request = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    print(request.json())
