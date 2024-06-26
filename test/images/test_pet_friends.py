from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200


def test_delete_pet_by_id(pet_id='f70212c3-4ced-4fa7-b4a5-17041a6f8454')
   """ Проверяем удаление питомца по id""" 
   
    pet_id = 'f3043661-b5a7-41b2-be7c-39e1e3141290'
    status, _ = pf.delete_pet(auth_key, pet_id)

    #запрашиваем список своих питомцев
    _, my_pets = pf.get_list_my_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_get_api_key_for_invalid_email_invalid_password(email=invalid_email, password=invalid_password):
    """Проверяем возможность входа при неверном логине и пароле """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    assert status == 400
      

def test_get_api_key_for_invalid_email_valid_password(email=invalid_email, password=valid_password):
     """Проверяем возможность входа при неверном логине и верном пароле """

     # Запрашиваем ключ api и сохраняем в переменую auth_key
      _, auth_key = pf.get_api_key(valid_email, valid_password)

    assert status == 400

     

def test_get_api_key_for_invalid_email_valid_password(email=valid_email, password=invalid_password):
    """Проверяем возможность входа при верном логине и неверном пароле """
   
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    assert status == 400
   

def test_get_api_key_for_invalid_user(email=valid_email, password=invalid_password):
    """Проверяем возможность входа при верном логине и неверном пароле """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
     _, auth_key = pf.get_api_key(valid_email, valid_password)
    
    assert status == 400

def test_add_new_pet_with_invalid_data_invalid_age(name='Персик', animal_type='двортерьер',
                                     age='65948776554'):
    """Проверяем что можно добавить питомца с  некорректными данными слишком большим числом в возрасте"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    

def test_add_new_pet_with_invalid_data_invalid_animal_type(name='Персик', animal_type='1568792855',
                                     age='4'):
    """Проверяем добавление питомца с  некорректными данными - некоректными данными в animal_type """
   
   # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
                                    
def test_add_new_pet_with_incomplete_data(name='Персик', animal_type=' ',
                                     age=' '):
    """Проверяем что можно добавить питомца с неполными данными"""
   
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_get_my_pets_with_valid_key(my_pets):
    """ Проверяем что запрос моих питомцев возвращает только список моих питомцев"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_my_pets(auth_key, my_pets)

    assert status == 200
    assert len(result['pets']) == my_pets

def test_delete_pet_by_id(pet_id='f70212c3-4ced-4fa7-b4a5-17041a6f8454')
   """ Проверяем удаление питомца по id""" 
   
    pet_id = 'f3043661-b5a7-41b2-be7c-39e1e3141290'
    status, _ = pf.delete_pet(auth_key, pet_id)

    #запрашиваем список своих питомцев
    _, my_pets = pf.get_list_my_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_pet_by_invalid_id(pet_id='f70212c3-4ced-4fa7-b4a5-17041a6f')
   """ Проверяем удаление питомца по  неверному id""" 
   
    pet_id = 'ff70212c3-4ced-4fa7-b4a5-17041a6f'
    status, _ = pf.delete_pet(auth_key, pet_id)

    #запрашиваем список своих питомцев
    _, my_pets = pf.get_list_my_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 400 и в списке питомцев нет такого  id  питомца
    assert status == 400
    assert pet_id not in my_pets.values()
