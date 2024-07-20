from telebot.handler_backends import State, StatesGroup


class RegisterStates(StatesGroup):
    full_name =State()
    birthdate = State()
    contact = State()


class CardStates(StatesGroup):
    card = State()


class CopyAdminState(StatesGroup):
    copy = State()




