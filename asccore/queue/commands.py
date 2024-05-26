from asccore.main import app, cli
from asccore.queue import AscWorker

from redis import Redis

from asccore.main import app

@cli.command("queue.work")
def package_test():
    worker = AscWorker(['default'], connection=app.make(Redis))
    worker.work(with_scheduler=True)
