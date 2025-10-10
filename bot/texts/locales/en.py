from __future__ import annotations

from aiogram.types import BotCommand

from bot.texts.base_enums import CallbackEnum


class MainMenuButtons(CallbackEnum):
    user_settings: str = '⚙️ Settings'
    get_params: str = '📊 Current Parameters'
    change_voice: str = '🎤 Change Voice'
    change_lang: str = '🌐 Language Selection'
    help: str = '❓ Help'

    @staticmethod
    def get_callback_name_suffix() -> str:
        return '_main'


class MainKbMessages:
    main_menu: str = '👻 Write a message in text or voice to get a response'
    get_params: str = '📊 Current Parameters'
    change_voice: str = '🎤 Choose Voice'
    change_lang: str = '🌐 Choose Language'
    help_info: str = ''

    @classmethod
    def get_help_info(cls, commands_info: str) -> str:
        return commands_info + cls.help_info

    def succes_update_str_parameter(param_name: str) -> str:
        return f'Parameter {param_name} updated'

# cancel button
class CancelButton(CallbackEnum):
    cancel: str = '❌ Cancel'
    cancel_success: str = '✅ Action cancelled'


class BackButton(CallbackEnum):
    back: str = '🔙 Back'
    back_to_main_menu: str = '🏠 Main Menu'

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
    answer_with_voice: str = '🔊 Answer with Voice'
    answer_with_text: str = '📄 Answer with Text'
    voice_name: str = ''


class KbParameterMessages:
    getparams_message: str = '📊 Current Parameters:\n'
    success_resetparams: str = '🔄 Parameters reset'

    def wait_input_str_parameter(parameter_name: str, curr_value: str) -> str:
        return (
            f'Current value of parameter {parameter_name}:\n{curr_value}\n'
            'Enter new value'
        )
    def out_of_range(parameter_name: str, max: float, min: float) -> str:
        return f'Value {parameter_name} cannot be greater than {max} and less than {min}'

    def invalid_parameter_message() -> str:
        return (
            'Invalid command, examples of correct commands:\n'
            '<code>/set top_k 40</code>\n'
            '<code>/reset enable_thinking</code>\n'
        )

    def str_not_is_number() -> str:
        return 'The passed parameter cannot be converted to a number'

    def parameter_is_missing(parameter_name: str) -> str:
        return f'Parameter {parameter_name} is missing in config or is not numeric'

    def success_update_parameter(updated_name: str, updated_value: str | float) -> str:
        return f'Parameter {updated_name} value updated to {updated_value}'


class ProcessMessages:
    convert_ogg_to_wav_error: str = 'An error occurred while converting ogg to wav ☹'
    speech_recognition_error: str = 'Failed to recognize speech ☹'
    no_ansewr_mode_selected: str = 'You need to select at least one output mode in generation settings'
    no_ansewr_mode_selected += ' ("Answer with Voice" and/or "Answer with Text")'
    wait_bot_answer = '⏳ Request accepted'

    def wait_bot_answer_with_position(position: int):
        return f'⏳ Request accepted, your position in queue: {position}'


class BotCommands:
    commands: list[BotCommand] = [
        BotCommand(command='start', description='start'),
        BotCommand(command='help', description='help'),
        BotCommand(command='settings', description='parameter settings'),
        BotCommand(command='getparams', description='view all current parameters'),
        BotCommand(command='resetparams', description='reset to default settings'),
    ]
    commands_info: str = '<b>General commands:</b>\n'
    for command in commands:
        commands_info += f'/{command.command} - {command.description}\n'
    commands_info += '''
<b>Setting parameters:</b>
/set <code>parameter_name number</code>
<b>Example:</b>
/set <code>temperature 0.5</code> - set temperature to 0.5
/set <code>enable_thinking 1</code> - enable thinking mode

<b>Resetting parameters:</b>
/reset <code>parameter_name</code>
<b>Example:</b>
/reset <code>temperature</code> - reset temperature to default value

<b>Generation parameters description:</b>
<code>temperature</code>, <code>top_p</code>, <code>top_k</code>, <code>repeat_penalty</code>, <code>max_tokens</code> - llama-cpp-python generation parameters
<code>enable_thinking</code> - enable/disable thinking mode (if Config.USE_HF_TOKENIZER=False then always on)
<code>show_thinking</code> - show thinking in response
<code>stream_llm_response</code> - output bot response in parts (works only if answer_with_text is active)
<code>system_prompt</code> - enter new system prompt
<code>user_lang</code> - change language
<code>voice_name</code> - select voice
<code>answer_with_text</code> - answer with text messages (must be enabled or at least one of both parameters)
<code>answer_with_voice</code> - answer with voice messages (must be enabled or at least one of both parameters)

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
