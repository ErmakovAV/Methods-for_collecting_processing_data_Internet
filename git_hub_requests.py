import requests
import json
from pprint import pprint
url = 'https://api.github.com/users/'
user = 'ErmakovAV'
response = requests.get(f'{url}{user}/repos')
# В переменную j_data сохраним полную информацию о репозиториях пользователя
j_data = response.json()
pprint(j_data)
# сделаем словарь, состоящий из указанных наименований репозиториев пользователя и
# сохраним полученный словарь в файл *.json
repos = {
    'name': []
}
for i in j_data:
    repos['name'].append(i['name'])
with open('repos_file.json', 'w') as file:
    json.dump(repos, file)
# выведем информацию о наименованиях репозиториев пользователя
print(f"Пользователь: {user} создал следующий список репозиториев: {repos['name']}")