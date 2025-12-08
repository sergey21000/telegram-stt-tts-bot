from __future__ import annotations

from aiogram.types import BotCommand

from bot.texts.base_enums import CallbackEnum


class MainMenuButtons(CallbackEnum):
    user_settings: str = '⚙️ Configure Settings'
    get_params: str = '📊 Current Settings'
    change_voice: str = '🎤 Change Voice'
    change_lang: str = '🌐 Select Language'
    help: str = '❓ Help'

@staticmethod
def get_callback_name_suffix() -> str:
    return '_main'


class MainKbMessages:
    main_menu: str = (
        "👻 <b>Welcome, bot usage options:</b>\n"
        "• Write a text or voice message to get a response.\n"
        "• Send an image and a caption, for example: «What is shown here?»\n"
        "• Send a video or audio file to get a text transcript of the audio track"
    )
    get_params: str = '📊 Current parameters'
    change_voice: str = '🎤 Select a voice'
    change_lang: str = '🌐 Select a language'
    help_info: str = ''

@classmethod
def get_help_info(cls, commands_info: str) -> str:
    return commands_info + cls.help_info

def succes_update_str_parameter(param_name: str) -> str:
    return f'Parameter {param_name} updated'


class CancelButton(CallbackEnum):
    cancel: str = '❌ Cancel'
    cancel_success: str = '✅ Action canceled'


class BackButton(CallbackEnum):
    back: str = '🔙 Back'
    back_to_main_menu: str = '🏠 Main menu'


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
    answer_with_voice: str = '🔊 Reply with voice'
    answer_with_text: str = '📄 Reply with text'
    voice_name: str = ''


class KbParameterMessages:
    getparams_message: str = '📊 Current parameters:\n'
    success_resetparams: str = '🔄 Parameters reset'

    def wait_input_str_parameter(parameter_name: str, curr_value: str) -> str:
        return (
            f'The current value of parameter {parameter_name} is: {curr_value}'
            'Enter a new value'
        )
    def out_of_range(parameter_name: str, max: float, min: float) -> str:
        return f'The value of {parameter_name} cannot be greater than {max} or less than {min}'

    def invalid_parameter_message() -> str:
        return (
            'Invalid command, examples of valid commands:'
            '<code>/set top_k 40</code>'
            '<code>/reset enable_thinking</code>'
        )

    def str_not_is_number() -> str:
        return 'The passed parameter cannot be converted to a number.'

    def parameter_is_missing(parameter_name: str) -> str:
        return f'Parameter {parameter_name} is missing from the config or is not a number'

    def success_update_parameter(updated_name: str, updated_value: str | float) -> str:
        return f'The value of parameter {updated_name} has been updated to {updated_value}'


class ProcessMessages:
    convert_media_to_wav_error: str = 'An error occurred while converting ogg to wav ☹'
    speech_recognition_error: str = 'Failed to recognize speech ☹'
    no_ansewr_mode_selected: str = 'You must select at least one output mode in the generation settings.'
    no_ansewr_mode_selected += ' ("Answer with voice" or/and "Answer" text")'
    wait_bot_answer: str = '⏳ Request accepted'
    convert_media_to_wav = 'Converting media to wav ...'
    stt = 'Recognizing text from speech...'
    llm = 'Generating response ...'
    tts = 'Speech synthesis ...'

def wait_bot_answer_with_position(position: int, n_max_concurrent_tasks: int) -> str:
    return (
        f'<b>⏳ Request accepted, your position in queue: {position}</b>\n'
        f'(number of concurrent requests processed: {n_max_concurrent_tasks})\n'
        '<b>Current status:</b>\n'
    )


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
/set <code>temperature 0.5</code> - set the temperature to 0.5
/set <code>enable_thinking 1</code> - enable thinking mode

<b>Resetting parameters:</b>
/reset <code>parameter_name</code>
<b>Example:</b>
/reset <code>temperature</code> - reset the temperature to the default value

<b>Description of generation parameters:</b>
<code>temperature</code>, <code>top_p</code>, <code>top_k</code>, <code>repeat_penalty</code>, <code>max_tokens</code> - llama-cpp-python generation parameters
<code>enable_thinking</code> - enable/disable Thinking mode
<code>show_thinking</code> - display thinking in the response
<code>stream_llm_response</code> - display the bot's response in parts (only works if answer_with_text is enabled)
<code>system_prompt</code> - enter a new system prompt
<code>user_lang</code> - change language
<code>voice_name</code> - select a voice
<code>answer_with_text</code> - respond with text messages (must be enabled, or at least one or both parameters)
<code>answer_with_voice</code> - respond with voice messages (must be enabled, or at least one or both parameters)
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
