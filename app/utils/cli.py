import click

from app import config, misc, services
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
    misc.runner.start(services.admin.count_alive_users_and_send_result(misc.bot, config.ADMIN_ID, User))
