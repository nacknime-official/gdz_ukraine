from aiogram.dispatcher.filters.state import State, StatesGroup

from app import config


class UserStates(StatesGroup):
    Grade = State()
    Subject = State()
    Author = State()
    Specification = State()
    Year = State()
    Main_topic = State()
    Sub_topic = State()
    Sub_sub_topic = State()
    Exercise = State()
    Solution = State()

    Keyboard = State()
    Wrapper_subjects = State()
    Wrapper_subject_entities = State()
    Wrapper_entities = State()


class AdminStates(StatesGroup):
    Input_send_all = State()
    Confirm_send_all = State()

    Input_send_notifs = State()
    Confirm_send_notifs = State()

    Input_block = State()
    Confirm_block = State()

    Input_unblock = State()
    Confirm_unblock = State()


quiz = [
    UserStates.Grade.state,
    UserStates.Subject.state,
    UserStates.Author.state,
    UserStates.Specification.state,
    UserStates.Year.state,
    UserStates.Main_topic.state,
    UserStates.Sub_topic.state,
    UserStates.Sub_sub_topic.state,
    UserStates.Exercise.state,
    UserStates.Solution.state,
]
state_messages = {
    UserStates.Grade.state: config.MSG_START,
    UserStates.Subject.state: config.MSG_SUBJECT,
    UserStates.Author.state: config.MSG_AUTHOR,
    UserStates.Specification.state: config.MSG_SPECIFICATION,
    UserStates.Year.state: config.MSG_YEAR,
    UserStates.Main_topic.state: config.MSG_MAIN_TOPIC,
    UserStates.Sub_topic.state: config.MSG_SUB_TOPIC,
    UserStates.Sub_sub_topic.state: config.MSG_SUB_SUB_TOPIC,
    UserStates.Exercise.state: config.MSG_EXERCISE,
}
