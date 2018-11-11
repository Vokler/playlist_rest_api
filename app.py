import json
import asyncio
import asyncpg
from aiohttp import web


def token_required(func):
    async def wrapper(self, *args, **kwargs):
        token = None

        if 'x-api-key' in self.request.headers:
            token = self.request.headers['x-api-key']

        if not token:
            result = {
                'message': 'Токен отсутсвует'
            }
            return web.Response(status=401, body=json.dumps(result), content_type='application/json')
        return await func(self, *args, **kwargs)

    return wrapper


class User(web.View):
    def __init__(self, request):
        super().__init__(request)
        self.pool = self.request.app['pool']

    async def post(self):
        try:
            data = await self.request.json()
            await self.pool.execute(
                "INSERT INTO users(email, first_name, last_name) VALUES ('{}', '{}', '{}');".format(data['email'],
                                                                                                    data['first_name'],
                                                                                                    data['last_name']))
            result = {
                'message': 'Пользователь успешно создан'
            }
            return web.Response(status=201, body=json.dumps(result), content_type='application/json')
        except Exception as e:
            result = {'message': str(e)}
            return web.Response(status=500, body=json.dumps(result), content_type='application/json')

    @token_required
    async def get(self):
        token = self.request.headers['x-api-key']

        try:
            async with self.pool.acquire() as connection:
                user = await connection.fetchrow("SELECT * from users WHERE api_key = '{}';".format(token))
                current_user = dict(user)
                user_data = {
                    'id': current_user['id'],
                    'email': current_user['email'],
                    'first_name': current_user['first_name'],
                    'last_name': current_user['last_name'],
                    'created': current_user['created'].strftime("%B %d, %Y, %H:%M"),
                    'is_active': current_user['is_active'],
                    'api_key': str(current_user['api_key'])
                }
                return web.Response(body=json.dumps(user_data), content_type='application/json')
        except Exception as e:
            result = {'message': str(e)}
            return web.Response(status=500, body=json.dumps(result), content_type='application/json')

    @token_required
    async def delete(self):
        token = self.request.headers['x-api-key']

        try:
            async with self.pool.acquire() as connection:
                is_active = await connection.fetchval("SELECT is_active from users WHERE api_key = '{}';".format(token))
                if is_active:
                    await connection.execute("UPDATE users SET is_active = FALSE WHERE api_key = '{}';".format(token))
                    result = {
                        'message': 'Пользователь удалён'
                    }
                    return web.Response(body=json.dumps(result), content_type='application/json')
                else:
                    result = {
                        'message': 'Пользователь с таким api-key уже удалён'
                    }
                    return web.Response(status=208, body=json.dumps(result), content_type='application/json')

        except Exception as e:
            result = {'message': str(e)}
            return web.Response(status=500, body=json.dumps(result), content_type='application/json')


class Album(web.View):
    def __init__(self, request):
        super().__init__(request)
        self.pool = self.request.app['pool']

    async def _get_user_id(self, token):
        async with self.pool.acquire() as connection:
            _user_id = await connection.fetchval("SELECT id FROM users WHERE api_key = '{}';".format(token))

        return _user_id

    @token_required
    async def post(self):
        try:
            token = self.request.headers['x-api-key']
            user_id = await self._get_user_id(token)

            data = await self.request.json()
            await self.pool.execute(
                "INSERT INTO albums(name, user_id, metadata)"
                "VALUES ('{}', {}, '{}');".format(data['name'], user_id, json.dumps(data['metadata'])))
            result = {
                'message': 'Альбом успешно создан'
            }
            return web.Response(status=201, body=json.dumps(result), content_type='application/json')
        except Exception as e:
            result = {'message': str(e)}
            return web.Response(status=500, body=json.dumps(result), content_type='application/json')

    @token_required
    async def get(self):
        try:
            token = self.request.headers['x-api-key']
            user_id = await self._get_user_id(token)
            async with self.pool.acquire() as connection:
                record_sql = await connection.fetch(
                    "SELECT * FROM albums WHERE user_id = {};".format(user_id))
                data_albums = []
                for item in record_sql:
                    data = {
                        'id': item['id'],
                        'name': item['name'],
                        'metadata': json.loads(item['metadata']),
                        'created': item['created'].strftime("%B %d, %Y, %H:%M"),
                        'updated': item['updated'].strftime("%B %d, %Y, %H:%M")
                    }
                    data_albums.append(data)

                if data_albums:
                    return web.Response(body=json.dumps(data_albums), content_type='application/json')
                else:
                    result = {'message': 'Нет альбомов у данного пользователя'}
                    return web.Response(status=204, body=json.dumps(result), content_type='application/json')
        except Exception as e:
            result = {'message': str(e)}
            return web.Response(status=500, body=json.dumps(result), content_type='application/json')

    @token_required
    async def put(self):
        try:
            token = self.request.headers['x-api-key']
            user_id = await self._get_user_id(token)
            async with self.pool.acquire() as connection:
                data = await self.request.json()
                await connection.execute(
                    "UPDATE albums SET name = '{}', metadata = '{}', updated = NOW()"
                    "WHERE id = {} AND user_id = {};".format(data['name'], json.dumps(data['metadata']), data['id'],
                                                             user_id))

                result = {
                    'message': 'Изменения внесены'
                }
            return web.Response(body=json.dumps(result), content_type='application/json')
        except Exception as e:
            result = {'message': str(e)}
            return web.Response(status=500, body=json.dumps(result), content_type='application/json')

    @token_required
    async def delete(self):
        try:
            async with self.pool.acquire() as connection:
                data = await self.request.json()
                await connection.execute(
                    "DELETE FROM albums WHERE id = {};".format(data['id']))

                result = {
                    'message': 'Альбом удалён'
                }

            return web.Response(body=json.dumps(result), content_type='application/json')
        except Exception as e:
            result = {'message': str(e)}
            return web.Response(status=500, body=json.dumps(result), content_type='application/json')


class Track(web.View):
    def __init__(self, request):
        super().__init__(request)
        self.pool = self.request.app['pool']

    async def _get_user_id(self, token):
        async with self.pool.acquire() as connection:
            _user_id = await connection.fetchval("SELECT id FROM users WHERE api_key = '{}';".format(token))

        return _user_id

    @token_required
    async def post(self):
        try:
            data = await self.request.json()
            await self.pool.execute(
                "INSERT INTO tracks(name, album_id)"
                "VALUES ('{}', {});".format(data['name'], data['album_id']))
            result = {
                'message': 'Трек добавлен'
            }
            return web.Response(body=json.dumps(result), content_type='application/json')
        except Exception as e:
            result = {'message': str(e)}
            return web.Response(status=500, body=json.dumps(result), content_type='application/json')

    @token_required
    async def get(self):
        try:
            token = self.request.headers['x-api-key']
            user_id = await self._get_user_id(token)
            async with self.pool.acquire() as connection:
                record_sql = await connection.fetch(
                    "SELECT tracks.id, tracks.name, tracks.created, tracks.updated "
                    "FROM tracks JOIN albums ON tracks.album_id = albums.id "
                    "WHERE albums.user_id = {};".format(user_id))
                data_tracks = []
                for item in record_sql:
                    data = {
                        'id': item['id'],
                        'name': item['name'],
                        'created': item['created'].strftime("%B %d, %Y, %H:%M"),
                        'updated': item['updated'].strftime("%B %d, %Y, %H:%M")
                    }
                    data_tracks.append(data)

                if data_tracks:
                    return web.Response(body=json.dumps(data_tracks), content_type='application/json')
                else:
                    result = {'message': 'Нет треков у данного пользователя'}
                    return web.Response(status=204, body=json.dumps(result), content_type='application/json')
        except Exception as e:
            result = {'message': str(e)}
            return web.Response(status=500, body=json.dumps(result), content_type='application/json')

    @token_required
    async def put(self):
        try:
            async with self.pool.acquire() as connection:
                data = await self.request.json()
                await connection.execute(
                    "UPDATE tracks SET name = '{}', updated = NOW()"
                    "WHERE id = {};".format(data['name'], data['id']))

                result = {
                    'message': 'Изменения внесены'
                }
            return web.Response(body=json.dumps(result), content_type='application/json')
        except Exception as e:
            result = {'message': str(e)}
            return web.Response(status=500, body=json.dumps(result), content_type='application/json')

    @token_required
    async def delete(self):
        try:
            async with self.pool.acquire() as connection:
                data = await self.request.json()
                await connection.execute(
                    "DELETE FROM tracks WHERE id = {};".format(data['id']))

                result = {
                    'message': 'Трек удалён'
                }

            return web.Response(body=json.dumps(result), content_type='application/json')
        except Exception as e:
            result = {'message': str(e)}
            return web.Response(status=500, body=json.dumps(result), content_type='application/json')


async def init_app():
    app = web.Application()
    DATABASE_URI = 'postgresql://user:password@host:port/database'
    app['pool'] = await asyncpg.create_pool(dsn=DATABASE_URI)
    app.router.add_view('/user', User)
    app.router.add_view('/album', Album)
    app.router.add_view('/track', Track)

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app)
