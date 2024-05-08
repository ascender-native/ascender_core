from asccore.support.service_provider import ServiceProvider

from redis import Redis

from asccore.main import config

class RedisServiceProvider(ServiceProvider):
    def register(self):
        host = config('database.redis.default.host')
        port = config('database.redis.default.port')
        db = config('database.redis.default.db')
        username = config('database.redis.default.username')
        password = config('database.redis.default.password')
        self.app.bind(Redis, lambda: Redis(host, port, db, password, username=username))

    def boot(self):
        pass