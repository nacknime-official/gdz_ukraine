from aiogram.utils.markdown import link


def user_link(text, user_id=None):
    if not user_id:
        user_id = text
    return link(str(text), f"tg://user?id={user_id}")
