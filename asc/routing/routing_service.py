from asc.support.service_provider import ServiceProvider
from asc.routing.router import Route, RouteList, Router

class RoutingServiceProvider(ServiceProvider):   

    async def register(self) -> None:
        await self._register_router()
    
    async def _register_router(self):
        self.app.bind(Route, RouteList)
        self.app.singleton(Router, Router)
        pass