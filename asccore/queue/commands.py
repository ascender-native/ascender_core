from asccore.main import app, cli
from asccore.queue import AscWorker

from redis import Redis

from asccore.contracts.kernel import Kernel
from asccore.main import app
from app.entity.channels import Post

@cli.command("queue.work")
def package_test():
    worker = AscWorker(['default'], connection=app.make(Redis))
    worker.work(with_scheduler=True)
