from collections import namedtuple
from typing import List, Optional, Union

from aiogram.utils.markdown import link

name_func = namedtuple("NameFunction", "name func")


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


def find_func_by_state_name(
    state_name: str, func_list: List[name_func]
) -> name_func.func:
    """
    Find function by state name in list of functions.
    Used for optimize redis storage - clean unneeded data
    from the state data.

    :param state_name:  state name
    :param func_list:   list of functions, in which we'll search

    :returns:           function
    """
    parsed_state_name = state_name.split(":")[-1].lower()
    for name_func in func_list:
        if name_func.name.startswith(parsed_state_name):
            return name_func.func
