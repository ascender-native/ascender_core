from asc.contracts.foundation.application import Application
from tortoise import Tortoise

class InvalidArgumentException(Exception):
    pass

class DatabaseManager():
    _app: Application
    _connections: dict = {}
    _reconnector: callable
    _extensions: list = []
    _models: list = []

    def __init__(self, app: Application) -> None:
        self._app = app
        self._reconnector = lambda connection: self.reconnect(connection.get_name_with_read_write_type())

    def reconnect(self, name = None):
        # TODO: disconnect
        if not name in self._connections:
            return self.connection(name)
        return self.refresh_connections(name)
    
    def refresh_connections(self, name):
        database, type = self._parse_connection_name(name)
        self._connections[name] = self.configure(
            self.make_connection(database), self.get_db_name(name))
        return self._connections[name]
    
    @staticmethod
    def get_db_name(name):
        match name:
            case 'pgsql': return 'postgres'
        return name
    
    def make_connection(self, name):
        config = self.configuration(name)
        if name in self._extensions:
            return self._extensions[name](config, name)
        return config
        
    def configuration(self, name):
        name = name or self.get_default_connection()
        config: dict = self._app.make('config')
        connections = config.get('database', {}).get('connections')
        db_config = connections.get(name, None)
        if db_config is None:
            raise InvalidArgumentException(f"Database connection [{name}] not configured.")
        return db_config

    async def connection(self, name: str = None):
        database, type = self._parse_connection_name(name)
        name = name or database
        if not name in self._connections:
            self._connections[name] = await self.configure(
                self.make_connection(database), self.get_db_name(name))
        return self._connections[name]
    
    async def configure(self, connecton, db_type: str):
        if (db_type == "sqlite"):
            obj = await Tortoise.init(
                db_url=db_type+'://{url}'.format(**connecton),
                modules={'models': self._models}
            )
        else:
            obj = await Tortoise.init(
                db_url=db_type+'://{username}:{password}@{host}:{port}/{database}'.format(**connecton),
                modules={'models': self._models}
            )
        await Tortoise.generate_schemas()
        return obj

    def _parse_connection_name(self, name: str):
        name = name or self.get_default_connection()
        return name.split('::', 1) if any(name.endswith(ending) for ending in ['::read', '::write']) else [name, None]
    
    def get_default_connection(self) -> str:
        config: dict = self._app.make('config')
        return config.get('database', {}).get('default', '')
