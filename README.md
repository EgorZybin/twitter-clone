# Клон Twitter

## Описание

Это клон Twitter, разработанный с использованием Python, FastAPI, PostgreSQL и других библиотек. Он предоставляет возможности:

Всего имеется 10 функциональных запросов сервиса:

1. POST /api/tweets - Добавить твит
2. POST /api/medias - Добавить медиафайл
3. DELETE /api/tweets/ - Удалить твит
4. POST /api/tweets//likes - Поставить лайк
5. DELETE /api/tweets//likes - Удалить лайк
6. POST /api/users//follow - Подписаться на пользователя
7. DELETE /api/users//follow - Отписаться от пользователя
8. GET /api/tweets - Получить ленту твитов
9. GET /api/users/me - Получить информацию о своем профиле
10. GET /api/users/ - Получить информацию о чужом профиле

После установки и запуска проекта вся документация доступна по адресу /docs/ сервера.


## Установка и запуск

Убедитесь, что у вас установлены Docker и docker-compose.

1. Клонируйте репозиторий:
````
git clone https://github.com/EgorZybin/twitter-clone.git
cd twitter-clone
````
2. Сборка и запуск контейнеров с приложением и базой данных:
````
docker-compose build
docker-compose up
````
## Использование

# 1. Добавление твита
````
POST /api/tweets
HTTP-Params:
api-key: str
{
“tweet_data”: string
“tweet_media_ids”: Array[int] // Опциональный параметр. Загрузка
картинок будет происходить по endpoint /api/media. Фронтенд будет
подгружать картинки туда автоматически при отправке твита и подставлять
id оттуда в json.
}
````
Запросом на этот endpoint пользователь будет создавать новый твит. Бэкенд будет его валидировать и сохранять в базу. В ответ должен вернуться id созданного твита.
````
{
“result”: true,
“tweet_id”: int
}
````
# 2. Endpoint для загрузки файлов из твита. Загрузка происходит через отправку формы
````
POST /api/medias
HTTP-Params:
api-key: str
form: file=”image.jpg”
````
В ответ должен вернуться id загруженного файла.
````
{
“result”: true,
“media_id”: int
}
````
# 3. Удаление твита
````
DELETE /api/tweets/<id>
HTTP-Params:
api-key: str
````
В ответ должно вернуться сообщение о статусе операции.
````
{
“result”: true
}
````
# 4. Пользователь может поставить отметку «Нравится» на твит.
````
POST /api/tweets/<id>/likes
HTTP-Params:
api-key: str
````
В ответ должно вернуться сообщение о статусе операции.
````
{
“result”: true
}
````
# 5. Пользователь может убрать отметку «Нравится» с твита.
````
DELETE /api/tweets/<id>/likes
HTTP-Params:
api-key: str
````
В ответ должно вернуться сообщение о статусе операции.
````
{
“result”: true
}
````
# 6. Пользователь может зафоловить другого пользователя.
````
POST /api/users/<id>/follow
HTTP-Params:
api-key: str
````
В ответ должно вернуться сообщение о статусе операции.
````
{
“result”: true
}
````
# 7. Пользователь может убрать подписку на другого пользователя.
````
DELETE /api/users/<id>/follow
HTTP-Params:
api-key: str
````
В ответ должно вернуться сообщение о статусе операции.
````
{
“result”: true
}
````
# 8. Пользователь может получить ленту с твитами.
````
GET /api/tweets
HTTP-Params:
api-key: str
````
В ответ должен вернуться json со списком твитов для ленты этого пользователя.
````
{
“result”: true,
"tweets": [
{
"id": int,
"content": string,
"attachments" [link_1, link_2,]
"author": {"id": int", "name": string}
“likes”: [{“user_id”: int, “name”: string}]
}]}
````
В случае любой ошибки на стороне бэкенда возвращайте сообщение следующего формата:
````
{
“result”: false,
“error_type”: str,
“error_message”: str
}
````
# 9. Пользователь может получить информацию о своём профиле:
````
GET /api/users/me
HTTP-Params:
api-key: str
````
В ответ получаем:
````
{
"result":"true",
"user":{
"id":"int",
"name":"str",
"followers":[{"id":"int", "name":"str"}],
"following":[{"id":"int", "name":"str"}]
}}
````
#10. Пользователь может получить информацию о другом профиле по его id
````
GET /api/users/<id>
````
В ответ получаем:
````
{
"result":"true",
"user":{
"id":"int",
"name":"str",
"followers":[{"id":"int", "name":"str"}],
"following":[{"id":"int", "name":"str"}]
}}
````
## Тесты

Все тесты написаны на библиотеке pytest (Подробнее: https://docs.pytest.org/en/7.2.x/contents.html)

- Для того чтобы запустить тесты нужно создать локальную базу данных PostgreSQL.
- В файле test/conftest.py указать все данные от вашей базы данных, такие как: Название базы данных, имя пользователя и пароль. 

# Тестирование

Для тестирования приложения надо в терминал написать команду:
````
pytest
````
Для более подробного запуска используйте команду:
````
pytest tests -vv
````
## Мониторинг приложения

Мониторинг приложения осуществляется с помощью Prometheus + Grafana

Чтобы просмотреть визуализированную панель, необходимо настроить Grafana:

1. Пройти по адресу http://localhost:3000 и зарегистрироваться в приложении (По умолчанию login: admin | password: admin).
2. Настроить источник данных (Prometheus) указав адрес http://prometheus:9090
3. Импортировать конфигурацию панели Grafana ./grafana/Dashboard_FastAPI.json

Подробнее: https://prometheus.io/docs/visualization/grafana/

## Авторы

Зыбин Егор (https://t.me/raizzep)