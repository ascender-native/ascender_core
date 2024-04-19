import click
from asc.main import cli, app
from asc.contracts.kernel import Kernel as KernelContract
from fastapi.routing import APIRouter, APIRoute
from tabulate import tabulate
from asc.routing.cli import RouteStyle

@cli.command("route.list")
def route_list():
    router: APIRouter = app.make(KernelContract)._router
    routes: list[APIRoute] = router.routes
    
    routes_tabulate = []
    for route in routes:
        routes_tabulate.append(RouteStyle(route).to_list())
        
    tabulate_ = tabulate(routes_tabulate, headers=['methods', 'url', 'name'], tablefmt="fancy_grid")
    click.echo(tabulate_)
