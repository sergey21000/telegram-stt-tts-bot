from aiogram.fsm.state import State, StatesGroup


class SettingsState(StatesGroup):
    user_settings = State()
    input_str_param = State()
    change_lang = State()
    change_voice = State()
