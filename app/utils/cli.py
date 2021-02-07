import click

from app import misc, services
from app.models.user import User


@click.group()
def cli():
    pass


@cli.command()
def run():
    misc.setup()
    misc.runner.start_polling()


@cli.command()
def count_alive_users():
    misc.setup()
    misc.runner.start(services.admin.scheduled_count_alive_users(misc.bot, User))
