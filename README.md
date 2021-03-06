# Rest API for playlist

Для успешной работы создать базу данных в PostgreSQL\
Создайте таблицы, запустив `python models.py`\
Запустите приложение `python app.py`

<h2>Описание API</h2>


### Создание нового пользователя

URL = [/user]\
Method = POST

_Параметры запроса_

| НАИМЕНОВАНИЕ | ОБЯЗАТЕЛЬНЫЙ? |
| ------ | ------ |
| email | + |
| first_name | + |
| last_name | + |

_Ответы сервера_

| КОД | ПАРАМЕТР | ОПИСАНИЕ |
| ------ | ------ | ------ |
| 201 | message | Возвращает сообщение об успешном создании пользователя
| 500 | message | Возвращает сообщение об ошибке

**Заметка!**\
Для следующих запросов обязательный параметр в HEADER:\
_x-api-key_

### Получение информации о пользовтаеле

URL = [/user]\
Method = GET

_Ответы сервера_

| КОД | ПАРАМЕТР | ОПИСАНИЕ |
| ------ | ------ | ------ |
| 200 | id, email, first_name, last_name, created, is_active, api_key| Возвращает информацию о пользоваателе
| 401 | message | Возвращает сообщение об отсутсвии токена (api-key)
| 500 | message | Возвращает сообщение об ошибке

### Удаление пользователя

URL = [/user]\
Method = DELETE

_Ответы сервера_

| КОД | ПАРАМЕТР | ОПИСАНИЕ |
| ------ | ------ | ------ |
| 204 | message | Возвращает информацию о том, что пользователь удалён
| 208 | message | Сообщает о том, что пользователь уже был удалён
| 401 | message | Возвращает сообщение об отсутсвии токена (api-key)
| 500 | message | Возвращает сообщение об ошибке

### Создание нового альбома

URL = [/album]\
Method = POST

_Параметры запроса_

| НАИМЕНОВАНИЕ | ОБЯЗАТЕЛЬНЫЙ? |
| ------ | ------ |
| name | + |
| metadata | + |

_Ответы сервера_

| КОД | ПАРАМЕТР | ОПИСАНИЕ |
| ------ | ------ | ------ |
| 201 | message | Возвращает сообщение об успешном создании альбома
| 401 | message | Возвращает сообщение об отсутсвии токена (api-key)
| 500 | message | Возвращает сообщение об ошибке

### Получение всех альбомов пользователя

URL = [/album]\
Method = GET

_Ответы сервера_

| КОД | ПАРАМЕТР | ОПИСАНИЕ |
| ------ | ------ | ------ |
| 200 | id, name, metadata, created, updated | Возвращает информацию об альбоме
| 204 | message | Возвращает информацию о том, что у пользователя нет альбомов
| 401 | message | Возвращает сообщение об отсутсвии токена (api-key)
| 500 | message | Возвращает сообщение об ошибке

### Изменение данных в альбоме

URL = [/album]\
Method = PUT

_Параметры запроса_

| НАИМЕНОВАНИЕ | ОБЯЗАТЕЛЬНЫЙ? |
| ------ | ------ |
| name | + |
| metadata | + |
| id | + |

_Ответы сервера_

| КОД | ПАРАМЕТР | ОПИСАНИЕ |
| ------ | ------ | ------ |
| 200 | message | Возвращает сообщение об успешном внесении изменений
| 401 | message | Возвращает сообщение об отсутсвии токена (api-key)
| 500 | message | Возвращает сообщение об ошибке

### Удаление альбома

URL = [/album]\
Method = DELETE

_Параметры запроса_

| НАИМЕНОВАНИЕ | ОБЯЗАТЕЛЬНЫЙ? |
| ------ | ------ |
| id | + |

_Ответы сервера_

| КОД | ПАРАМЕТР | ОПИСАНИЕ |
| ------ | ------ | ------ |
| 204 | message | Возвращает сообщение об успешном удалении альбома
| 401 | message | Возвращает сообщение об отсутсвии токена (api-key)
| 500 | message | Возвращает сообщение об ошибке

### Добавление нового трека

URL = [/track]\
Method = POST

_Параметры запроса_

| НАИМЕНОВАНИЕ | ОБЯЗАТЕЛЬНЫЙ? |
| ------ | ------ |
| name | + |
| album_id | + |

_Ответы сервера_

| КОД | ПАРАМЕТР | ОПИСАНИЕ |
| ------ | ------ | ------ |
| 201 | message | Возвращает сообщение об успешном добавлении трека
| 401 | message | Возвращает сообщение об отсутсвии токена (api-key)
| 500 | message | Возвращает сообщение об ошибке

### Получение всех треков пользователя

URL = [/track]\
Method = GET

_Ответы сервера_

| КОД | ПАРАМЕТР | ОПИСАНИЕ |
| ------ | ------ | ------ |
| 200 | id, name, created, updated | Возвращает информацию об альбоме
| 204 | message | Возвращает информацию о том, что у пользователя нет треков
| 401 | message | Возвращает сообщение об отсутсвии токена (api-key)
| 500 | message | Возвращает сообщение об ошибке

### Изменение данных в треке

URL = [/track]\
Method = PUT

_Параметры запроса_

| НАИМЕНОВАНИЕ | ОБЯЗАТЕЛЬНЫЙ? |
| ------ | ------ |
| name | + |
| id | + |

_Ответы сервера_

| КОД | ПАРАМЕТР | ОПИСАНИЕ |
| ------ | ------ | ------ |
| 200 | message | Возвращает сообщение об успешном внесении изменений
| 401 | message | Возвращает сообщение об отсутсвии токена (api-key)
| 500 | message | Возвращает сообщение об ошибке

### Удаление трека

URL = [/track]\
Method = DELETE

_Параметры запроса_

| НАИМЕНОВАНИЕ | ОБЯЗАТЕЛЬНЫЙ? |
| ------ | ------ |
| id | + |

_Ответы сервера_

| КОД | ПАРАМЕТР | ОПИСАНИЕ |
| ------ | ------ | ------ |
| 204 | message | Возвращает сообщение об успешном удалении трека пользователя
| 401 | message | Возвращает сообщение об отсутсвии токена (api-key)
| 500 | message | Возвращает сообщение об ошибке
