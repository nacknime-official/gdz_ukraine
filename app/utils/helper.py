from typing import Optional, Union

from aiogram.utils.markdown import link


def get_user_link(user_id: Union[str, int], text: Optional[str] = None) -> str:
    """
    Get markdown link on a user
    Used in the admin's block commands

    :param user_id:   user's id
    :param text:      text of the link

    :returns:         link
    """
    if not text:
        text = user_id
    return link(str(text), f"tg://user?id={user_id}")
