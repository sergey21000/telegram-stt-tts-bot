from __future__ import annotations

from aiogram.types import BotCommand

from bot.texts.base_enums import CallbackEnum


class MainMenuButtons(CallbackEnum):
    user_settings: str = '⚙️ Настройка параметров'
    get_params: str = '📊 Текущие параметры'
    change_voice: str = '🎤 Смена голоса'
    change_lang: str = '🌐 Выбор языка'
    help: str = '❓ Справка'

    @staticmethod
    def get_callback_name_suffix() -> str:
        return '_main'


class MainKbMessages:
    main_menu: str = '👻 Напишите сообщение текстом или голосом чтобы получить ответ'
    get_params: str = '📊 Текущие параметры'
    change_voice: str = '🎤 Выберите голос'
    change_lang: str = '🌐 Выберите язык'
    help_info: str = ''

    @classmethod
    def get_help_info(cls, commands_info: str) -> str:
        return commands_info + cls.help_info

    def succes_update_str_parameter(param_name: str) -> str:
        return f'Параметр {param_name} обновлен'


class CancelButton(CallbackEnum):
    cancel: str = '❌ Отмена'
    cancel_success: str = '✅ Действие отменено'


class BackButton(CallbackEnum):
    back: str = '🔙 Назад'
    back_to_main_menu: str = '🏠 Главное меню'

    @staticmethod
    def get_callback_name_suffix() -> str:
        return '_cancel'


class UserBtnTexts:
    temperature: str = ''
    top_p: str = ''
    top_k: str = ''
    repeat_penalty: str = ''
    max_tokens: str = ''
    enable_thinking: str = ''
    show_thinking: str = ''
    stream_llm_response: str = ''
    system_prompt: str = ''
    user_lang: str = ''
    answer_with_voice: str = '🔊 Отвечать голосом'
    answer_with_text: str = '📄 Отвечать текстом'
    voice_name: str = ''


class KbParameterMessages:
    getparams_message: str = '📊 Текущие параметры:\n'
    success_resetparams: str = '🔄 Параметры сброшены'

    def wait_input_str_parameter(parameter_name: str, curr_value: str) -> str:
        return (
            f'Текущее значение параметра {parameter_name}:\n{curr_value}\n'
            'Введите новое значение'
        )
    def out_of_range(parameter_name: str, max: float, min: float) -> str:
        return f'Значение {parameter_name} не может быть больше {max} и меньше {min}'

    def invalid_parameter_message() -> str:
        return (
            'Неправильная команда, примеры правильных команд:\n'
            '<code>/set top_k 40</code>\n'
            '<code>/reset enable_thinking</code>\n'
        )

    def str_not_is_number() -> str:
        return 'Переданный параметр не может быть преобразован в число'

    def parameter_is_missing(parameter_name: str) -> str:
        return f'Параметр {parameter_name} отсутствует в конфиге или является не числовым'

    def success_update_parameter(updated_name: str, updated_value: str | float) -> str:
        return f'Значение параметра {updated_name} обновлено на {updated_value}'


class ProcessMessages:
    convert_ogg_to_wav_error: str = 'Произошла ошибка при конвертации ogg в wav ☹'
    speech_recognition_error: str = 'Не удалось распознать речь ☹'
    no_ansewr_mode_selected: str = 'Необходимо выбрать хотя бы один режим вывода в настройках генерации'
    no_ansewr_mode_selected += ' ("Отвечать голосом" или/и "Отвечать текстом")'
    wait_bot_answer = '⏳ Запрос принят'

    def wait_bot_answer_with_position(position: int):
        return f'⏳ Запрос принят, ваше место в очереди: {position}'


class BotCommands:
    commands: list[BotCommand] = [
        BotCommand(command='start', description='start'),
        BotCommand(command='help', description='справка'),
        BotCommand(command='settings', description='настройка параметров'),
        BotCommand(command='getparams', description='просмотр всех текущих параметров'),
        BotCommand(command='resetparams', description='сбросить настройки по умолчанию'),
    ]
    commands_info: str = '<b>Общие параметры:</b>\n'
    for command in commands:
        commands_info += f'/{command.command} - {command.description}\n'
    commands_info += '''
<b>Установка параметров:</b>
/set <code>название_параметра число</code>
<b>Пример:</b>
/set <code>temperature 0.5</code> - установить температуру на 0.5
/set <code>enable_thinking 1</code> - включить режим размышлений

<b>Сброс параметров:</b>
/reset <code>название_параметра</code>
<b>Пример:</b>
/reset <code>temperature</code> - сбросить температуру на значение по умолчанию

<b>Описание параметров генерации:</b>
<code>temperature</code>, <code>top_p</code>, <code>top_k</code>, <code>repeat_penalty</code>, <code>max_tokens</code> - параметры генерации llama-cpp-python
<code>enable_thinking</code> - включение/отключение режима размышлений (если Config.USE_HF_TOKENIZER=False то всегда вкл)
<code>show_thinking</code> - выводить размышления в ответе
<code>stream_llm_response</code> - выводить ответ бота частями (работает только если активен answer_with_text)
<code>system_prompt</code> - ввести новый системный промт
<code>user_lang</code> - смена языка
<code>voice_name</code> - выбор голоса
<code>answer_with_text</code> - отвечать текстовыми сообщениями (должен быть включен или хотя бы один или оба параметра)
<code>answer_with_voice</code> - отвечать голосовыми сообщениями (должен быть включен или хотя бы один или оба параметра)

'''


class Texts:
    MainMenuButtons: type[MainMenuButtons] = MainMenuButtons
    MainKbMessages: type[MainKbMessages] = MainKbMessages
    CancelButton: type[CancelButton] = CancelButton
    BackButton: type[BackButton] = BackButton
    UserBtnTexts: type[UserBtnTexts] = UserBtnTexts
    KbParameterMessages: type[KbParameterMessages] = KbParameterMessages
    ProcessMessages: type[ProcessMessages] = ProcessMessages
    BotCommands: type[BotCommands] = BotCommands
