# user_id = 'created id'
# access_token = 'created token'
import requests

def get_response(address):
    # Функция для получения и проверки ответа от сервера
    # :param address:адрес сервера
    # :return:ответ от сервера
    response = requests.get(address)
    if response.status_code == 200:
        return response
    else:
        print(f'Запрос к адресу {response.url} завершился ошибкой: {response.status_code} '
              f'Текст ошибки: {response.text}')
        return response
def get_user_profile_id(user: str, token: str) -> int:
    # функция для получения user_id по тестовому имени пользователя
    # :param user: имя пользователя
    # :param token: токен для обращения к vk.com
    # :return: цифровой id пользователя
    url = f'https://api.vk.com/method/users.get?' \
          f'user_id={user}&' \
          f'access_token={token}&' \
          f'v=5.131'
    response = get_response(url)
    user_id = response.json()['response'][0]['id']
    return user_id
def get_user_subscriptions(user_id: int, token: str) -> dict:
    # получение подписок пользователя
    # :param user_id: цифровой id пользователя
    # :param token: токен, для обращения к vk.com
    # :return: словарь с идентификаторами пользователей и
    # публичных страниц из списка подписок пользователя
    url = f'https://api.vk.com/method/users.getSubscriptions?' \
          f'user_id={user_id}&' \
          f'access_token={token}&' \
          f'v=5.131'
    response = get_response(url)
    user_subscriptions = response.json()['response']
    return user_subscriptions
def get_user_groups(data: dict) -> list:
    # извлечение списка групп из подписок пользователя и получение их названий
    # :param data: словарь с идентификатором
    # :return: список названий публичных страниц, которые входят в список подписок пользователя
    user_group_list = data['groups']['items']
    user_group_list = parse_groups_name(user_group_list)
    return user_group_list
def parse_groups_name(group_list):
    # преобразование цифровых идентификаторов публичных страниц в наименование
    group_list_in_str = ','.join(map(str, group_list))
    api_url = f'https://api.vk.com/method/groups.getById?' \
              f'group_ids={group_list_in_str}&' \
              f'access_token={access_token}&' \
              f'v=5.131'
    response = get_response(api_url)
    group_list = response.json()['response']
    groups_name_list = []
    for group in group_list:
        groups_name_list.append(group['name'])
    return groups_name_list
def main(token):
    # основной скрипт для работы
    # :param token: токен для работы с vk.com
    user_name = input('Enter your vk.com user_name or user_id: ')
    if not user_name.isdigit():
        user_name = get_user_profile_id(user_name, token)
    user_subscriptions = get_user_subscriptions(user_name, token)
    user_group_list = get_user_groups(user_subscriptions)
    for group in user_group_list:
        print(group)
if __name__ == '__main__':
    access_token = 'Enter your token access'
    main(access_token)