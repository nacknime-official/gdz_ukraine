from contextlib import contextmanager

from aiogram.utils.exceptions import (
    BotBlocked,
    CantInitiateConversation,
    ChatNotFound,
    UserDeactivated,
)


class UserIsNotWithUsException(Exception):
    def __init__(self, error_message: str) -> None:
        self.error_message = error_message


@contextmanager
def catch_user_is_not_with_us_exceptions():
    """
    Context manager, used in broadcasting and sending messages
    with counting alive users

    Usage:
        try:
            with catch_user_is_not_with_us_exceptions():
                await bot.send_photo(...)
        except UserIsNotWithUsException as e:
            error = e.error_message

    """
    error = ""
    try:
        yield
    except BotBlocked:
        error = "This user blocked the bot"
    except UserDeactivated:
        error = "This user is no longer in TG"
    except ChatNotFound:
        error = "Chat not found or the user has deleted his account"
    except CantInitiateConversation:
        error = "CantInitiateConversation"

    if error:
        raise UserIsNotWithUsException(error)
